import datetime
import json
import os.path
import unittest

from pdf_ocr_service.jobs.domains import TokenPosition


def time_cost(func):
    def wrapper(*args, **kwargs):
        start_time = datetime.datetime.now()
        res = func(*args, **kwargs)
        over_time = datetime.datetime.now()
        print('current Function {0} run time is {1}'.format(func.__name__, (over_time - start_time).total_seconds()))
        return res

    return wrapper


class StrTest(unittest.TestCase):
    @time_cost
    def test_endwith(self):
        demo_str = 'dev/xxx/sdfd/'
        print(demo_str.endswith('/'))
        demo_str = 'dev/xxx/sdfd'
        if not demo_str.endswith('/'):
            print('join str...')
            demo_str = os.path.join(demo_str, 'adfds')
        print(demo_str)

    def test_assign(self):
        arr = [1, 2, 3, 4]
        var = True if len(arr) > 0 else False
        print(var)
        arr = []
        var = True if len(arr) > 0 else False
        print(var)
        arr = None
        var = True if arr is not None and len(arr) > 0 else False
        print(var)

    def test_file_name(self):
        target_file_name = 'aaa..afd.adfd.pdf'
        target_file_name = target_file_name if not target_file_name.endswith(".pdf") else target_file_name[:len(
            target_file_name) - 4]
        print(target_file_name)
        target_file_name = 'aaa..afd.adfd'
        target_file_name = target_file_name if not target_file_name.endswith(".pdf") else target_file_name[:len(
            target_file_name) - 4]
        print(target_file_name)
        target_file_name = '.pdf'
        target_file_name = target_file_name if not target_file_name.endswith(".pdf") else target_file_name[:len(
            target_file_name) - 4]
        target_file_name = target_file_name if not len(target_file_name) <= 0 else 'dsafsadf'
        print(target_file_name)

    def test_positions(self):
        positions: list[TokenPosition] = []
        print(json.dumps(positions))
        position = TokenPosition(left=1123.12312, right=12312.00, top=12312.00, bottom=1231231.0)
        print(position.__json__())
        for i in range(10):
            position = TokenPosition(left=1123.12312, right=12312.00, top=12312.00, bottom=1231231.0)
            positions.append(position)

        json_value = json.dumps(positions, default=lambda obj: obj.__json__())
        print(json_value)
        print(type(json_value))

    def test_position_sort(self):
        def position_to_values2(p: dict):
            value = p['bottom'] * 10000 + p['left'] * 1000 + p['top'] * 100 + p['right'] * 10
            return value

        json_str = '[{"left": 450.552001953125, "right": 564.601318359375, "top": 63.59453582763672, "bottom": 73.64922332763672},{"left": 450.552001953125, "right": 564.601318359375, "top": 63.59453582763672, "bottom": 73.64922332763672}, {"left": 477.4840087890625, "right": 564.7015380859375, "top": 85.73053741455078, "bottom": 95.78522491455078}, {"left": 518.8079833984375, "right": 566.9474487304688, "top": 96.24253845214844, "bottom": 106.29722595214844}, {"left": 498.65496826171875, "right": 564.551513671875, "top": 118.66453552246094, "bottom": 128.71922302246094}, {"left": 71.94999694824219, "right": 536.564208984375, "top": 156.03599548339844, "bottom": 180.61412048339844}, {"left": 72.0, "right": 560.484130859375, "top": 181.333984375, "bottom": 205.912109375}, {"left": 72.0, "right": 167.9013671875, "top": 206.63198852539062, "bottom": 231.21011352539062}, {"left": 81.0, "right": 154.95608520507812, "top": 287.3737487792969, "bottom": 300.7799987792969}, {"left": 409.407958984375, "right": 487.63641357421875, "top": 156.03599548339844, "bottom": 180.61412048339844}, {"left": 72.0, "right": 150.22848510742188, "top": 181.333984375, "bottom": 205.912109375}, {"left": 81.3499984741211, "right": 109.36798095703125, "top": 301.1727294921875, "bottom": 314.5789794921875}, {"left": 81.3499984741211, "right": 154.10610961914062, "top": 364.7677307128906, "bottom": 378.1739807128906}, {"left": 81.0, "right": 283.7259826660156, "top": 393.24072265625, "bottom": 406.64697265625}, {"left": 81.0, "right": 301.2579650878906, "top": 407.03973388671875, "bottom": 420.44598388671875}, {"left": 81.0, "right": 123.27590942382812, "top": 420.8387145996094, "bottom": 434.2449645996094}, {"left": 107.8499984741211, "right": 142.14373779296875, "top": 658.4979858398438, "bottom": 669.4979858398438}, {"left": 81.0, "right": 264.7458190917969, "top": 434.6377258300781, "bottom": 448.0439758300781}, {"left": 81.0, "right": 210.40599060058594, "top": 448.4367370605469, "bottom": 461.8429870605469}, {"left": 81.0, "right": 211.87384033203125, "top": 462.2357177734375, "bottom": 475.6419677734375}, {"left": 107.8499984741211, "right": 255.4818115234375, "top": 658.4979858398438, "bottom": 669.4979858398438}, {"left": 254.98599243164062, "right": 261.6300354003906, "top": 656.7899780273438, "bottom": 669.0790405273438}, {"left": 261.6299743652344, "right": 291.9028015136719, "top": 658.4979858398438, "bottom": 669.4979858398438}, {"left": 291.406982421875, "right": 298.051025390625, "top": 656.7899780273438, "bottom": 669.0790405273438}, {"left": 298.05096435546875, "right": 327.7847900390625, "top": 658.4979858398438, "bottom": 669.4979858398438}, {"left": 327.2889709472656, "right": 333.9330139160156, "top": 656.7899780273438, "bottom": 669.0790405273438}, {"left": 333.9329528808594, "right": 368.6717834472656, "top": 658.4979858398438, "bottom": 669.4979858398438}, {"left": 368.27496337890625, "right": 374.91900634765625, "top": 656.7899780273438, "bottom": 669.0790405273438}, {"left": 374.9189758300781, "right": 420.64678955078125, "top": 658.4979858398438, "bottom": 669.4979858398438}, {"left": 420.4479675292969, "right": 427.0920104980469, "top": 656.7899780273438, "bottom": 669.0790405273438}, {"left": 427.09197998046875, "right": 500.9330749511719, "top": 658.4979858398438, "bottom": 669.4979858398438}]'
        pos_list_dict: list[dict] = json.loads(json_str)
        pos_list_dict.sort(key=position_to_values2)
        print(pos_list_dict)
        positions: list[TokenPosition] = list()
        for d in pos_list_dict:
            position = TokenPosition(
                left=d.get('left'),
                right=d.get('right'),
                top=d.get('top'),
                bottom=d.get('bottom')
            )
            if not position in positions:
                positions.append(position)
        print(len(positions))

        def position_to_values(p: TokenPosition):
            value = p.bottom * 10000 + p.left * 1000 + p.top * 100 + p.right * 10
            return value

        def position_cmp(p1: TokenPosition, p2: TokenPosition):
            p1_value = position_to_values(p1)
            p2_value = position_to_values(p2)
            return p1_value - p2_value

        # sorted_list = sorted(positions, key=functools.cmp_to_key(
        #     lambda x, y: position_cmp(x, y)))
        # print(sorted_list)
        positions.sort(key=position_to_values)
        print(positions)

    def test_demo(self):
        def myFunc(e):
            return e['year']

        cars = [
            {'car': 'Ford', 'year': 2005},
            {'car': 'Mitsubishi', 'year': 2000},
            {'car': 'BMW', 'year': 2019},
            {'car': 'VW', 'year': 2011}
        ]
        cars.sort(key=myFunc)
        print(cars)

    def test_position_equals(self):
        top = 63.59453582763672
        bottom = 73.64922332763672
        left = 450.552001953125
        right = 564.601318359375

        p1: TokenPosition = TokenPosition(
            top=top,
            bottom=bottom,
            left=left,
            right=right
        )

        p2: TokenPosition = TokenPosition(
            top=top,
            bottom=bottom,
            left=left,
            right=right
        )

        print(p1 == p2)

        p2: TokenPosition = TokenPosition(
            top=63.69453582763672,
            bottom=bottom,
            left=left,
            right=right
        )
        print(p1 == p2)

        print(p2.__json__())
