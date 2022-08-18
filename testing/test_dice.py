from plugins.random.dice import build, evaluate
from core.error import Error

expr = "("

result = evaluate(build(expr))

if isinstance(result, int):
    print(result)
elif isinstance(result, Error):
    print(result.what)
else:
    print(result)