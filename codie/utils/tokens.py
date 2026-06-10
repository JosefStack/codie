# MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

INPUT_PRICE = 0.15
COMPLETE_PRICE = 0.60


class TokenTracker:
    def __init__(self):
        self.prompt_tokens = 0
        self.completion_tokens = 0

    def add(self, usage):
        self.prompt_tokens += usage.prompt_tokens
        self.completion_tokens += usage.completion_tokens
    
    @property
    def total_tokens(self):
        return self.prompt_tokens + self.completion_tokens

    def cost(self) -> str:
        input_cost = (self.prompt_tokens / 1_000_000) * INPUT_PRICE
        output_cost = (self.completion_tokens / 1_000_000) * COMPLETE_PRICE
        total_cost = input_cost + output_cost

        color = "red" if total_cost > 0.01 else "green"

        return (
            f"Total Tokens: {self.total_tokens:,}\n"
            f"Input Tokens: {self.prompt_tokens:,} (Cost: ${input_cost:.4f})\n"
            f"Output Tokens: {self.completion_tokens:,} (Cost: ${output_cost:.4f})\n"
            f"Total Cost: [{color}]${total_cost:.4f}[/{color}]"
        )
