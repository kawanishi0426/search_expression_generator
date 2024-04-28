import flet as ft
import json
import os
import re
import copy

class SearchExpressionGeneratorApp():
    def __init__(self, config_path:str, page: ft.Page) -> None:
        # Load configuration file
        curr_dir = os.getcwd()
        with open(curr_dir + '/' + config_path, 'r', encoding='utf_8') as f:
            self.config = json.load(f)
        # Create app
        self.page = page
        # Settings
        self._init_parameters()
        self._window_setting()
        # Execution
        self.run()
        
    def _init_parameters(self):
        self.word_num = 0
        self.keyword_offset_num = 3
        self.indices = self.config["input_row"]
        
    def run(self):
        self._add_search_expression()
        self.page.controls.append(ft.Text(value="キーワード登録"))
        self._add_new_line_button()
        for _ in range(self.config['default_line_num']):
            self._add_search_word()
    
    def _add_search_expression(self):
        self.page.controls.append(ft.Text(value="検索式"))
        create_btn = ft.ElevatedButton(
            text="Create", on_click=self._update_expression)
        exp_in = ft.TextField(width=450, label=f"", autofocus=True)
        self.page.controls.append(ft.Row([create_btn, exp_in]))
        self.page.controls.append(ft.TextField(width=600, label=f"", autofocus=True))
        self.page.update()
    
    def _update_expression(self, e):
        # 
        ctrls = self.page.controls[1].controls
        txt_exp = ctrls[1].value
        # 
        str_list = re.split(r'[\(\)\+\-\*]', txt_exp)
        # 
        num_list = []
        for s in str_list:
            try:
                num = int(s)
            except Exception:
                continue
            num_list.append(str(num))
        # 
        txt_exp_swapped = copy.deepcopy(txt_exp)
        for s in num_list:
            idx = self.keyword_offset_num + int(s)
            ctrls = self.page.controls[idx].controls
            txt_out = ctrls[self.indices["txt_out"]].value
            # txt_exp_swapped.replace(s, txt_out, 1)
            txt_exp_swapped = re.sub(f'[{s}]', txt_out, txt_exp_swapped)
        self.page.controls[2].value = txt_exp_swapped
        self.page.update()
    
    def _add_new_line_button(self):
        btn = ft.ElevatedButton(text="+", on_click=self._add_search_word)
        self.page.controls.append(btn)
        self.page.update()

    def _delete_line(self, e=None):
        self.word_num -= 1
        for n in range(e.control.data+1, len(self.page.controls)-1):
            ctrls = self.page.controls[n].controls
            ctrls[self.indices["idx"]].value = f'{int(ctrls[self.indices["idx"]].value)-1:02d}'
            ctrls[self.indices["del_btn"]].data -= 1
        self.page.controls.pop(e.control.data)
        self.page.update()

    def _add_search_word(self, e=None):
        self.word_num += 1
        index = ft.Text(value=f"{self.word_num:02d}")

        cat_list = []
        for key in self.config['category'].keys():
            cat_list.append(ft.dropdown.Option(self.config['category'][key]))
        pd = ft.Dropdown(
            width=150,
            value =None,
            options=cat_list
            )
        elment_idx = len(self.page.controls)-1
        del_btn = ft.ElevatedButton(
            text="-", on_click=self._delete_line, data=elment_idx)
        txt_in = ft.TextField(width=150, label=f"", autofocus=True)
        update_btn = ft.ElevatedButton(
            text="update", on_click=self._update_txt_out, data=elment_idx)
        sw_near = ft.Switch(label='近傍探索', value=False)
        txt_in_2 = ft.TextField(width=150, label=f"", autofocus=True)
        near_num = ft.TextField(width=50, label=f"1-99", value=1, autofocus=True)
        sw_front_back = ft.Switch(label='前後入替', value=False)
        txt_out = ft.TextField(width=200, label=f"", autofocus=True)

        row = ft.Row([index, del_btn, pd, txt_in, sw_near, txt_in_2, 
                      near_num, sw_front_back, update_btn, txt_out])
        self.page.controls.insert(-1, row)
        self.page.update()
    
    def _update_txt_out(self, e):
        target_idx = e.control.data
        ctrls = self.page.controls[target_idx].controls
        # カテゴリを取得する
        category = ctrls[self.indices["category"]].value
        for key in self.config["category"].keys():
            if category == self.config["category"][key]:
                cat_str = key
        # '全文'のみモードを取得する
        if category == self.config["category"]["TX"]:
            if ctrls[self.indices["sw_near"]].value:
                txt_in_2 = ctrls[self.indices["txt_in_2"]].value
                near_num = ctrls[self.indices["near_num"]].value
                if txt_in_2 == '':
                    pass
                elif ctrls[self.indices["sw_front_back"]].value:
                    # 入力文字列に追加する
                    txt_in = ctrls[self.indices["txt_in"]].value
                    ctrls[self.indices["txt_out"]].value = f'{txt_in},{near_num}N,{txt_in_2}/{cat_str}'
                    self.page.update()
                    return
                else:
                    # 入力文字列に追加する
                    txt_in = ctrls[self.indices["txt_in"]].value
                    ctrls[self.indices["txt_out"]].value = f'{txt_in},{near_num}C,{txt_in_2}/{cat_str}'
                    self.page.update()
                    return
            else:
                pass
        else:
            pass
        # 入力文字列に追加する
        txt_in = ctrls[self.indices["txt_in"]].value
        ctrls[self.indices["txt_out"]].value = f'{txt_in}/{cat_str}'
        self.page.update()
        return   

    def _window_setting(self):
        self.page.window_width = self.config['window']["width"]
        self.page.window_height = self.config['window']["height"]
    
