from plugins.replier.template_render import *

set_key = "{die}, 我是{name}"
set_cm = "你是{name}, 而我是{die}"

argmap = {}

template = extract_argmap(set_key, argmap)

print("set_key", set_key)
print("argmap", argmap)

message = "SiriusNEO, 我是啥比！"

print(template_match(message, template))

collected_map = collect(message, template, argmap)

print("collected_map", collected_map)

print("reply", render(set_cm, collected_map))