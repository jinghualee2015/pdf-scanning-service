import unittest


def demo_fun(arg_1: int = 0, **kwargs):
    print(f"arg1={arg_1}")
    for key in kwargs.keys():
        print(f"key={key}  value={kwargs.get(key)}")


def demo_fun2(*args, **kwargs):
    # print(print(f"arg1={arg_1} arg2={arg_2}\n"))
    for ind, value in enumerate(args):
        print(f"ind={ind}, value={value}")

    for key in kwargs.keys():
        print(f"key={key}  value={kwargs.get(key)}")


def demo_fun3(arg_1, arg_2, *args, **kwargs):
    print(print(f"arg1={arg_1} arg2={arg_2}\n"))
    for ind, value in enumerate(args):
        print(f"ind={ind}, value={value}")

    for key in kwargs.keys():
        print(f"key={key}  value={kwargs.get(key)}")


class KwargsTest(unittest.TestCase):

    def test_demo1(self):
        arg1 = 10
        extra_args = {
            'test': 123123.1231,
            'block_number': 10,
            'tokens': [
                1, 2, 3, 4, 5, 6
            ],
        }
        demo_fun(arg_1=arg1, **extra_args)

    def test_demo11(self):
        arg1 = 10
        demo_fun(arg_1=arg1, test='asdfadsfas', block_number=21312, tokens=[1, 2, 3, 4, 5, 6])

    def test_demo2(self):
        arg1 = 10
        arg2 = 'hello word'
        extra_args = {
            'test': 123123.1231,
            'block_number': 10,
            'tokens': [
                1, 2, 3, 4, 5, 6
            ],
        }
        arg_arr = ["!2321", 12213, "OK", 123.12]
        demo_fun2(arg_1=arg1, arg_2=arg2, **extra_args)

    def test_demo3(self):
        arg1 = 10
        arg2 = 'hello word'
        extra_args = {
            'test': 123123.1231,
            'block_number': 10,
            'tokens': [
                1, 2, 3, 4, 5, 6
            ],
        }
        arg_arr = ["!2321", 12213, "OK", 123.12]
        demo_fun3(arg_1=arg1, arg_2=arg2, arg3="dafdas", arg4="adfads", **extra_args)
