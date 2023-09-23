from haystack.pipelines import GenerativeQAPipeline


class SimpleGenerativeQAPipeline(GenerativeQAPipeline):

    def run(self, *args, **kwargs):
        output = super().run(*args, **kwargs)
        return self.get_results_from_output(output)

    @staticmethod
    def get_results_from_output(output):
        return output['answers'][0].answer
