class _TestPythonObj:
    def method(self):
        print("Hi World!")

def test_basic_python():
    obj:_TestPythonObj = _TestPythonObj()

    a = obj.method
    b = obj.method

    if a is b:
        print("methods: a is b ")
    else:
        print("methods: a is NOT b ")

    if a == b:
        print("methods: a == b ")
    else:
        print("methods: a != b ")

    method_set = set()
    method_set.add(a)
    method_set.add(b)
    if len(method_set) == 1:
        print("sets appear to use == for item comparisons")
    elif len(method_set) == 2:
        print("sets appear to use is for item comparison")

    assert True