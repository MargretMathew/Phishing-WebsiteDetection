class PrimeGenerator:
    def __init__(self):
        self.primes = []
        self.current = 1

    def __iter__(self):
        return self

    def __next__(self) -> int:
        candidate = self.current + 1
        while True:
            for prime in itertools.takewhile(lambda p: candidate >= p**2, self.primes):
                if candidate % prime == 0:
                    break
            else:
                self.primes.append(candidate)
                self.current = candidate
                break

            candidate += 1

        return self.current
