def foo(qux):
    def bar(func):
        def baz(*args):
            try:
                print("Morty")
                func(*args)
                return args
            except qux:
                print("Town")
                return args[0]
            else:
                print("Locos")
            finally:
                print(":D")
        return baz
    return bar

class FunError(ZeroDivisionError):
    pass

@foo(ZeroDivisionError)
def double_fun(*args):
    raise FunError("Doble diversion")

try:
    r = double_fun("hola")
except FunError:
    r = "Evil Morty"

print(r)