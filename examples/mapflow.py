
from metaflow import FlowSpec, step
from metaflow_magicdir import magicdir


class MagicDirMapFlow(FlowSpec):
    """Show how magic directories work with foreach"""

    @step
    def start(self):
        self.step_num = range(5)
        self.next(self.write, foreach='step_num')

    @magicdir(dir='my_map_dir')
    @step
    def write(self):
        self.step_idx = self.input # metaflow gives self.input a value from `step_num` from the prior step
        with open(f'my_map_dir/{self.step_idx}.txt', 'w') as f:
            f.write(f'this is step {self.step_idx}')
        self.next(self.read)

    @magicdir(dir='my_map_dir')
    @step
    def read(self):
        print('file contents:', open(f'my_map_dir/{self.step_idx}.txt').read())
        self.next(self.join)
    
    @step
    def join(self, inputs):
        print(f"step numbers were: {[i.step_idx for i in inputs]}")
        self.next(self.end)

    @step
    def end(self): pass

if __name__ == "__main__":
    MagicDirMapFlow()

if __name__ == "__main__":
    MagicDirMapFlow()
