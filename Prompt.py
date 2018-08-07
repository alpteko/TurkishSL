import re
import copy
import unidecode


class Prompt:
    p = re.compile('\(.*\)')

    def __init__(self, n, t, c, d=None, is_group=False):
        if is_group:
            self.number = n
            self.interval = t
            self.content = c
            self.sentence = self.parser2list(c)
            self.descriptions = [desc for desc in d if desc]
        else:
            self.number = n
            # "00:00:60.200 --> 00:00:80.50"
            # TODO parse time maybe?
            self.interval = [l.strip() for l in t.split('-->')]

            self.descriptions = []
            c_updated = []
            for l in c:
                # Speech... Storing this info might be useful...
                # Ex: "(Brock)"
                l = l[1:] if l.startswith('-') else l
                m = self.p.search(l)
                while m:
                    self.descriptions.append(m.group()[1:-1])
                    l = (l[:m.span()[0]] + l[m.span()[1]:]).strip()
                    m = self.p.search(l)
                c_updated.append(l)

            self.descriptions = None if len(self.descriptions) == 0 else self.descriptions
            self.content = ' '.join(c_updated)
            self.sentence = self.parser2list(self, self.content)
        self.is_group = is_group

    def extend_content(self, other_content):
        return '{} {}'.format(
            self.content[:-3] if self.content.endswith('...') else self.content,
            other_content[3:] if other_content.startswith('...') else other_content
        )

    def __add__(self, other):
        combined = None
        if self.is_group:
            combined = copy.copy(self)

            combined.number.append(other.number)
            combined.interval.append(other.interval)
            combined.descriptions.append(other.descriptions)
            combined.content = self.extend_content(other.content)
        else:
            combined = Prompt([self.number, other.number],
                              [self.interval, other.interval],
                              self.extend_content(other.content),
                              [self.descriptions, other.descriptions],
                              True)
        return combined

    def __repr__(self):
        return '{}: {} || {}\n{}\n'.format(self.number, self.descriptions,
                                           self.interval, self.content)

    @staticmethod
    def parser2list(self, s):
        s = re.sub(r'[^\w\s]', '', s).lower()
        ####
        ## Stemming
        tokens = unidecode.unidecode(s).split()

        hasNumbers = lambda x :  any(char.isdigit() for char in x)
        return [token for token in tokens if not(hasNumbers(token))]
