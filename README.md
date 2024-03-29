### Cybervox Virtual Assistant
Cybervox Virtual Assistant é o primeiro projeto Opensource brasileiro de assistente virtual. Ela ainda é um bebê que está aprendendo a engatinhar. Contribua com o seu desenvolvimento.
#### Config
##### 1. Start
Para configurar o projeto e baixar as dependências só executar o 
``$ bin/setup.sh``
##### 2. Edit enviroment and actions file
###### 2.1 Autenticação CyberVox
Entre em contato conosco para obter as chaves do CyberVox.
```
Header de email: [Chaves de Acesso] Cybervox Virtual Assistant
email: contato@cybervox.ai
```
E em seguida configure as credenciais de acesso da seguinte forma.
```
CLIENT_ID=< provided client id >
CLIENT_SECRET=< provided client secret >
```
###### 2.2 Escolhendo o device de audio
Escolha o seu microfone ou device de audio e coloque no ``.env`` o ``INPUT_DEVICE_INDEX``. Execute o seguinte comando para verificar sua lista de devices.
```
$ python3 bin/list_devices.py
```
Caso tenha alguma dúvida, utilize o que estiver com o `DEVICE_NAME: default`.
###### 2.3 Wake Up Word
É possível utilizar dois Wake Up Words: "Hey Cyber" ou "Jarvis". No entanto, "Hey Cyber" é temporário.
```
# Jarvis = 0, Hey Cyber = 1
WAKE_UP_WORD=< 0 or 1 >
```
##### 3. Editando os comandos de voz
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
###### 3.1 Integrando ao [KeyApp](https://keyapp.ai/)
Ainda estamos melhorando essa integração. Em breve será liberado uma nova versão.
##### 4. Run
Execute usando
```
$ python3 app.py
```
E diga "Hey Cyber, quem é você?" para um teste inicial.
##### 5. Teste local
Por padrão, o ```action.json``` já vem com uma ação de Speech Command. Caso queira testa-lo, utilize 
```
$ python3 bin/simple_server_text.py
```
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
- [ ] Raspberry test.
- [x] Adicionar "Hey Cyber" como wake up.
- [ ] Remover "Jarvis" como wake up word.
- [ ] Testar em um sistema Windows.