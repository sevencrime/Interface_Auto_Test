from functools import reduce

fn = lambda x, code=',': reduce(lambda x, y: [str(i)+code+str(j) for i in x for j in y], x)
fns = lambda x, code=',': reduce(lambda x, y: [str(i)+code+str(j) for i in x for j in y], x)


def lists_combination(lists, code=''):
    '''输入多个列表组成的列表, 输出其中每个列表所有元素可能的所有排列组合
    code用于分隔每个元素'''
    try:
        import reduce
    except:
        from functools import reduce
        
    def myfunc(list1, list2):
        return [str(i)+code+str(j) for i in list1 for j in list2]
    return reduce(myfunc, lists)




list1 = ['onedi', '', 100, '*aSoLV(W', '*aSoLV(WM', '*aS']
list2 = ['15033331111', '', 100, '0', '1', '1abc']
list3 = [10, 10.11, 0, -1, 18, 19, 20, 30]


tests = {'name': ['onedi', '', 100, '(i8(@eLL', '(i8(@eLL4', '(i8(@eL'], 'phone': ['15033331111', '', 100, '0', '1', '1abc'], 'age': [10, 10.11, 0, -1, 18, 19, 20, 30]}


# print(fn([list3, list2, list1]))
# print(fn([i for i in tests.values()]))


# for i in fn([i for i in tests.values()]):
#     print(dict(zip([k for k in tests.keys()], i.split(","))))


if not isinstance('111', int):
    print("ssss")


