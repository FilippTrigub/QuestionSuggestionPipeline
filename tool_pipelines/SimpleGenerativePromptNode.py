from haystack.nodes import PromptNode


class SimpleGenerativePromptNode(PromptNode):

    def run(self, *args, **kwargs):
        output = super().run(*args, **kwargs)
        return self.get_results_from_output(output)

    @staticmethod
    def get_results_from_output(output):
        return output[0]['results'][0]
