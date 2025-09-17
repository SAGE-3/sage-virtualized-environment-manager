#!/usr/bin/env python3
import asyncio
import websockets
import subprocess
import threading
import queue
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AudioStreamer:
    def __init__(self):
        self.clients = set()
        self.audio_queue = queue.Queue(maxsize=50)  # Slightly larger queue
        self.ffmpeg_process = None
        self.running = True
        self.restart_lock = threading.Lock()
        
    def start_audio_capture(self):
        """Start FFmpeg to capture audio from PulseAudio"""
        # cmd = [
        #     'ffmpeg',
        #     '-f', 'pulse',
        #     '-i', 'default',
        #     '-f', 's16le',           # Raw PCM - no encoding latency
        #     '-ar', '44100',
        #     '-ac', '2',
        #     '-fflags', 'nobuffer',   # Disable input buffering
        #     '-flags', 'low_delay',   # Low delay mode
        #     '-probesize', '32',      # Minimal probe size
        #     '-analyzeduration', '0', # Skip analysis
        #     '-'
        # ]
        
        cmd = [
            'parec',
            '--format=s16le',
            '--rate=44100',
            '--channels=2',
            '--latency-msec=15', 
        ]

        try:
            self.ffmpeg_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=0
            )
            
            # Start thread to read audio data
            threading.Thread(target=self._read_audio_data, daemon=True).start()
            logger.info("Audio capture started")
            
        except Exception as e:
            logger.error(f"Failed to start audio capture: {e}")
    
    def _restart_ffmpeg(self):
        """Restart FFmpeg process if it fails"""
        with self.restart_lock:
            if self.ffmpeg_process:
                try:
                    self.ffmpeg_process.terminate()
                    self.ffmpeg_process.wait(timeout=5)
                except:
                    try:
                        self.ffmpeg_process.kill()
                    except:
                        pass
                self.ffmpeg_process = None
            
            # Clear the queue to avoid stale data
            while not self.audio_queue.empty():
                try:
                    self.audio_queue.get_nowait()
                except queue.Empty:
                    break
            
            # Restart audio capture
            threading.Event().wait(1)  # Brief pause before restart
            self.start_audio_capture()
    
    def _read_audio_data(self):
        """Read audio data from FFmpeg and queue it"""
        chunk_size = 4096  # Keep original chunk size (23ms at 44.1kHz stereo)
        consecutive_failures = 0
        max_failures = 5
        
        while self.running and self.ffmpeg_process:
            try:
                # Check if process is still alive
                if self.ffmpeg_process.poll() is not None:
                    logger.warning("FFmpeg process died, attempting restart...")
                    self._restart_ffmpeg()
                    continue
                
                data = self.ffmpeg_process.stdout.read(chunk_size)
                if data:
                    consecutive_failures = 0  # Reset failure counter on success
                    
                    # Simple queue management - drop oldest if full
                    if self.audio_queue.full():
                        try:
                            self.audio_queue.get_nowait()
                        except queue.Empty:
                            pass
                    
                    try:
                        self.audio_queue.put_nowait(data)
                    except queue.Full:
                        pass  # Skip if still full
                else:
                    # No data received - might indicate a problem
                    consecutive_failures += 1
                    if consecutive_failures >= max_failures:
                        logger.warning(f"No audio data for {max_failures} consecutive reads, restarting FFmpeg...")
                        self._restart_ffmpeg()
                        consecutive_failures = 0
                    
            except Exception as e:
                logger.error(f"Error reading audio data: {e}")
                consecutive_failures += 1
                if consecutive_failures >= max_failures:
                    logger.warning("Too many consecutive failures, restarting FFmpeg...")
                    self._restart_ffmpeg()
                    consecutive_failures = 0
                else:
                    # Brief pause before retry
                    threading.Event().wait(0.1)
    
    async def handle_client(self, websocket, path):
        """Handle new WebSocket client connection"""
        logger.info(f"New audio client connected: {websocket.remote_address}")
        self.clients.add(websocket)
        
        try:
            await websocket.wait_closed()
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.clients.discard(websocket)
            logger.info(f"Audio client disconnected: {websocket.remote_address}")
    
    async def broadcast_audio(self):
        """Broadcast audio data to all connected clients"""
        while self.running:
            try:
                # Get audio data with minimal timeout
                try:
                    data = self.audio_queue.get(timeout=0.01)  # 10ms timeout
                except queue.Empty:
                    await asyncio.sleep(0.002)  # 2ms sleep
                    continue
                
                if self.clients:
                    # Send to all clients concurrently
                    disconnected = set()
                    send_tasks = []
                    
                    for client in self.clients.copy():
                        send_tasks.append(self._send_to_client(client, data, disconnected))
                    
                    if send_tasks:
                        await asyncio.gather(*send_tasks, return_exceptions=True)
                    
                    # Remove disconnected clients
                    self.clients -= disconnected
                    
            except Exception as e:
                logger.error(f"Error in broadcast loop: {e}")
                await asyncio.sleep(0.002)
    
    def stop(self):
        """Stop the audio streamer"""
        self.running = False
        if self.ffmpeg_process:
            try:
                self.ffmpeg_process.terminate()
                self.ffmpeg_process.wait(timeout=5)
            except:
                try:
                    self.ffmpeg_process.kill()
                except:
                    pass
    
    async def _send_to_client(self, client, data, disconnected):
        """Send data to a single client"""
        try:
            await client.send(data)
        except websockets.exceptions.ConnectionClosed:
            disconnected.add(client)
        except Exception as e:
            logger.error(f"Error sending to client: {e}")
            disconnected.add(client)

async def main():
    streamer = AudioStreamer()
    
    try:
        # Start audio capture
        streamer.start_audio_capture()
        
        # Start WebSocket server
        server = await websockets.serve(
            streamer.handle_client,
            "0.0.0.0",
            7772,
            ping_interval=None,  # Disable ping for lower latency
            ping_timeout=None,
            max_size=None,
            compression=None     # Disable compression for lower latency
        )
        
        logger.info("Audio WebSocket server started on port 7772")
        
        # Start broadcasting
        broadcast_task = asyncio.create_task(streamer.broadcast_audio())
        
        # Wait for server
        await server.wait_closed()
        
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    finally:
        streamer.stop()

if __name__ == "__main__":
    asyncio.run(main())