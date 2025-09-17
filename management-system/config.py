# Production container mapping


class ContainerConfigs:
   tag = ':amd64'
   
   prod_container_mapping = {
       'vnc-connect': f'ghcr.io/sage-3/cosage-vnc{tag}',
       'sage-firefox': f'ghcr.io/sage-3/cosage-firefox{tag}',
       'vnc-x11-blender': f'ghcr.io/sage-3/cosage-blender{tag}',
   }
   
   supported_containers = {
       'vnc-connect': {
           "environment": {
               'TARGET_IP': '0.0.0.0',
               'TARGET_PORT': '5900',
           },
       },
       'sage-firefox': {
           "environment": {
               'FIREFOX_URLS': [],
               'FIREFOX_THEME': 0,
               'CALLBACK_ID': '',
               # 'CALLBACK_ADDR': '',
               # 'CALLBACK_TOKEN': '',
               # 'CALLBACK_CMD': '',
               # 'CALLBACK_URL_BASE': '',
               # 'CALLBACK_URL_V2': '',
               # 'FIREFOX_STARTPAGE': "www.google.com",
           },
       },
       # 'vnc-x11-doom': {
       #     "environment": {
       #     },
       # },
       'vnc-x11-blender': {
           "environment": {
           },
       }
   }
   
   @staticmethod
   def dev_map_func(name):
       return name  # convert to lambda later if you want
   
   @staticmethod
   def prod_map_func(name):
       return ContainerConfigs.prod_container_mapping[name]