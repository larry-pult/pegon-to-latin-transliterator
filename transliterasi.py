from pegon import Pegon


class PegonToLatinBigramTransliterator:
    START_OF_LINE_TOKEN = "<SOL>"

    def __init__(self):
        self.x_tokens = []
        self.y_tokens = []
        self.probability_map = dict()
        self.token_pair_map = dict()

    def train(self, x_train, y_train):
        assert len(x_train) == len(y_train), "Length of x_train and y_train must be equal"

        for i in range(len(x_train)):
            pegon_word = x_train[i]
            latin_word = y_train[i]

            x_tokens_current = self.tokenize_pegon(pegon_word)
            y_tokens_current = self.tokenize_latin(latin_word)

            if len(x_tokens_current) != len(y_tokens_current):
                continue

            self.x_tokens.extend(x_tokens_current)
            self.y_tokens.extend(y_tokens_current)

        self.calculate_token_pair_map(self.x_tokens, self.y_tokens)

    def predict(self, x_test):
        if isinstance(x_test, str):
            return self.predict_word(x_test)

        y_pred = []
        for word in x_test:
            prediction = self.predict_word(word)
            y_pred.append(prediction)

        return y_pred

    def predict_word(self, word):
        if word.isascii():
            return word

        x_tokens = self.tokenize_pegon(word)
        y = ""

        for token in x_tokens:
            try:
                y += self.token_pair_map[token]
            except KeyError:
                y += token[1]

        return y

    def tokenize_pegon(self, word):
        tokens = []
        i = 0
        n = len(word)
        prev_token = self.START_OF_LINE_TOKEN
        curr_token = self.START_OF_LINE_TOKEN

        while i < n:
            prev_token = curr_token
            curr_token = word[i]

            if i < n - 1 and (word[i], word[i + 1]) in Pegon.DIGRAPH_LIST:
                curr_token += word[i + 1]
                i += 1

            i += 1

            tokens.append((prev_token, curr_token))

        return tokens

    def tokenize_latin(self, word):
        tokens = []
        i = 0
        n = len(word)

        # looping from start to end of word, collecting pairs of tokens in each iteration
        while i < n:
            token = word[i]

            # combine polygraphs into an individual token
            while i < n - 2 and (word[i + 2] == "-"):
                token += word[i + 1] + word[i + 2]
                i += 2
            while i < n - 1 and (token == "^" or "_" in (word[i], word[i + 1])):
                token += word[i + 1]
                i += 1

            tokens.append(token)

            i += 1

        return tokens

    def calculate_token_pair_map(self, x_tokens, y_tokens):
        n = len(x_tokens)
        probability_map = dict()
        token_pair_map = dict()

        # calculate probability map
        for i in range(n):
            x_token = x_tokens[i]
            y_token = y_tokens[i]

            probability_map.setdefault(x_token, dict())
            probability_map[x_token].setdefault(y_token, 0)

            probability_map[x_token][y_token] += 1

        for x in probability_map:
            total = 0
            for y in probability_map[x]:
                total += probability_map[x][y]
            for y in probability_map[x]:
                probability_map[x][y] /= total

        # calculate token pair map
        for x in probability_map:
            y_max = -1
            p_max = -1
            for y in probability_map[x]:
                count = probability_map[x][y]
                if count > p_max:
                    p_max = count
                    y_max = y
            token_pair_map[x] = y_max

        self.probability_map = probability_map
        self.token_pair_map = token_pair_map
