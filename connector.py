from nene_copen_v2 import NN
import nn_gen

nn = None

ENTRY_TABLES = ['TypeScript', 'Java', 'ApacheConf', 'JavaScript', 'Makefile',
'Perl', 'Lua', 'Shell', 'Python', 'Nginx', 'HTML', 'Elixir', 'Ruby', 'C',
'C++', 'TeX', 'Objective-C', 'R', 'CSS', 'C#', 'ActionScript', 'Go', 'PHP']

def start():
    nn = NN([5, 30, 2])
    t = nn_gen.DataGen()
    data = t.gen(3000)
    nn.gradientDescent(data, 30, 5, 3.0)
    print "NN entranada"

def transform_langs(langs):
    res = []
    for lang in ENTRY_TABLES:
        res.append(lang in langs)
    return res

def train(langs, answer):
    if nn is not None:
        nn.correct(transform_langs(langs), answer)
    else:
        raise Exception('NN hasn\'t been started.')

def test(langs):
    if nn is not None:
        return nn.getAnswer(transform_langs(langs))
    else:
        raise Exception('NN hasn\'t been started.')
