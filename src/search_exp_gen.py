from app import SearchExpressionGeneratorApp as SE
import flet as ft

def main(page: ft.Page):
    _ = SE(config_path="config.json", page=page)

ft.app(target=main)

