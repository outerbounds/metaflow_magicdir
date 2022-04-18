
from metaflow import FlowSpec, step
from metaflow_magicdir import magicdir


class MagicDirFlow(FlowSpec):

    @magicdir(dir='mydir')
    @step
    def start(self):
        with open('mydir/output1', 'w') as f:
            f.write('hello world')
        with open('mydir/output2', 'w') as f:
            f.write('hello world again')
        self.next(self.end)

    @magicdir(dir='mydir')
    @step
    def end(self):
        print('first', open('mydir/output1').read())
        print('second', open('mydir/output1').read())

if __name__ == "__main__":
    MagicDirFlow()
