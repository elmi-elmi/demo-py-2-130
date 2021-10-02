class IgnoreMe(Exception):
    pass


class CloseCoroutine(Exception):
    pass


# def delegator():
#     result = yield from echo()
#     yield 'sub generator closed and returned: ', result
#     print('delegator closing...')
#
#
# def echo():
#     output = None
#     try:
#         while True:
#             try:
#                 receive = yield output
#                 print(receive)
#             except IgnoreMe:
#                 output = "I'm ignoring you!"
#             else:
#                 output = None
#     except CloseCoroutine:
#         return "coroutine was closed"
#     except GeneratorExit:
#         return "from a GeneratorExit"


def echo():
    while True:
        receive = yield
        print(receive)


def delegator():
    while True:
        try:
            yield from echo()
        except ValueError:
            print('delegator got the value error')


d = delegator()
# next(d)
d.__next__()
d.throw(ValueError)
d.send('rock')
# d.throw(IgnoreMe)

class WriteAverage(Exception):
    pass


def averager(out_file):
    total = 0
    count = 0
    average = None
    with open(out_file, 'w') as f:
        f.write('count, average\n')
        while True:
            try:
                received = yield average
                total += received
                count += 1
                average = total / count
            except WriteAverage:
                if average is not None:
                    print('saving average to file:', average)
                    f.write(f'{count}, {average}\n')


avg = averager('sample.csv')
next(avg)
avg.send(1)
avg.send(2)
avg.throw(WriteAverage)
avg.send(3)
avg.send(2)
avg.throw(WriteAverage)
avg.close()
with open('sample.csv') as f:
    print('------')
    for row in f:
        print(row.strip())

# def delegator():
#     yield from averager('sample.csv')
#
