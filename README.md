### Cybervox Virtual Assistant
Cybervox Virtual Assistant é o primeiro projeto Opensource brasileiro de assistente virtual. Ela ainda é um bebê que está aprendendo a engatinhar. Contribua com o seu desenvolvimento.
#### Config
##### Start
Para configurar o projeto e baixar as dependências só executar o 
``$ bin/setup.sh``
##### Edit enviroment and actions file
Edite o ``.env`` com suas chaves do Cybervox.
Para criar os comandos de voz edite o ``actions.json`` como o exemplo abaixo
~~~json
{
    "data": [
        {
            "name": "liga a luz do quarto",
            "url": "http://0.0.0.0:8080/quarto",
            "method": "POST",
            "staticPayload": {
                "response": "Ligando a luz do quarto."
            }
        }
    ]
}
~~~
###### Com o [KeyApp](https://keyapp.ai/)
As variáveis``KEY_TOKEN, KEY_PORTAL`` no ``.env`` são obrigatórios caso queira fazer integração com o [KeyApp](https://keyapp.ai/). Crie um portal e ações. O título das ações será o seu comando de voz.
###### Escolhendo o device de audio
Escolha o seu microfone ou device de audio e coloque no ``.env`` o ``INPUT_DEVICE_INDEX``.
```
$ python3 bin/list_device.py
```
##### Run
Execute usando
```
$ python3 app.py
```
E diga "Jarvis" para iniciar o comando descrito no seu ``actions.json``.
##### Teste local
Por padrão, o ```action.json``` já vem com uma ação de Speech Command. Caso queira testa-lo, utilize 
``$ python3 bin/simple_server_text.py``
#### To do
- [x] Ajuste detecção de voz.
- [ ] Redução de ruído (https://github.com/werman/noise-suppression-for-voice).
- [x] Ajuste no loop de voz. Não fechar o programa quando acabar uma frase.
- [x] Comparação de texto para disparar uma ação.
- [ ] Docker.
- [x] Text to speech.
- [ ] Testes.
- [x] Integração com o KeyApp.
- [x] Envio do binário ao Cybervox. Atualmente é um aiff convertido para wav, gambiarra :see_no_evil:.
- [ ] NLP.
- [ ] Raspberry test.
- [ ] Adicionar "Cyber" como wake up.
- [ ] Remover "Jarvis" como wake up word.
- [ ] Testar em um sistema Windows.