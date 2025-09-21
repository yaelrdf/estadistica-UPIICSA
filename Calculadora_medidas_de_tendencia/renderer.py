from nicegui import ui

ui.table.from_pandas(df).classes('max-h-200')

with ui.pyplot(figsize=(6, 4)) as plot:
    grapher(df)

ui.run()