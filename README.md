### Cybervox Virtual Assistant
Cybervox Virtual Assistant é o primeiro projeto Opensource brasileiro de assistente virtual. Ela ainda é um bebê que está aprendendo a engatinhar. Contribua com o seu desenvolvimento.
#### Config
##### Start
Para configurar o projeto e baixar as dependências só executar o 
``$ bin/setup.sh``
##### Edit enviroment and actions file
Entre em contato conosco para obter as chaves do CyberVox.
```
Header de email: [Chaves de Acesso] Cybervox Virtual Assistant
email: contato@cybervox.ai
```
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
###### Escolhendo o device de audio
Escolha o seu microfone ou device de audio e coloque no ``.env`` o ``INPUT_DEVICE_INDEX``.
```
$ python3 bin/list_devices.py
```
Caso tenha alguma dúvida, utilize o que estiver com o `DEVICE_NAME: default`.
###### Integrando ao [KeyApp](https://keyapp.ai/)
Ainda estamos melhorando essa integração. Em breve será liberado uma nova versão.
##### Run
Execute usando
```
$ python3 app.py
```
E diga "Hey Cyber, quem é você?" para um teste inicial.
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