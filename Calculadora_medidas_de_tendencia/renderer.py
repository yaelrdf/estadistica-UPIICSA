from nicegui import ui

def index():
    # CSS styles for the header
    ui.add_head_html('''
    <style>
        .header-container {
            background: linear-gradient(90deg, #008552 0%, #9ebd13 100%);
            padding: 5px 50px;
            display: flex;
            align-items: center;
            gap: 30px;
            width: 100%;
            margin: 0;
            justify-content: space-between;
        }
        .logo-title-group {
            display: flex;
            align-items: center;
            gap: 30px;
        }
        .header-button-container {
            display: flex;
            align-items: center;
        }
        .logo-image {
            width: 80px;
            height: 80px;
            padding: 0px;
        }
        .header-title {
            color: white;
            font-size: 2.3em;
            font-weight: bold;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            letter-spacing: 1px;
        }
        .header-button {
            background: rgba(255, 255, 255, 0.2);
            border: 2px solid rgba(255, 255, 255, 0.3);
            color: white;
            padding: 10px 20px;
            border-radius: 25px;
            font-weight: bold;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
        }
        .header-button:hover {
            background: rgba(255, 255, 255, 0.3);
            border-color: rgba(255, 255, 255, 0.5);
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        }
        .nicegui-content {
            margin: 0 !important;
            padding: 0 !important;
        }
    </style>
    ''')
    
    # Create the header container
    with ui.row().classes('header-container'):
        #Logo y titulo
        with ui.row().classes('logo-title-group'):
            ui.image('Calculadora_medidas_de_tendencia/image.png').classes('logo-image')
            ui.html('<h1 class="header-title">Calculadora de medidas de tendencia central</h1>')
        
        #Boton
        with ui.row().classes('header-button-container'):
            ui.button('Menú', icon='menu', on_click=lambda: ui.notify('Un refresh esta por llegar')).classes('button')
    ui.space()
    
