### Cybervox Virtual Assistant
Cyber é o primeiro projeto Opensource brasileiro de assistente virtual. Ela ainda é um bebê que está aprendendo a engatinhar. Contribua com o seu desenvolvimento.
#### Config
##### Start
Execute ``bin/setup.sh``
##### Edit enviroment and actions file
Edite ``.env`` e ``actions.json`` para com suas configuração.
##### Run
```
    python3 app.py
```
##### Test
Caso queira testar com algum Speech Command utilize ``python bin/simple_server_text.py``.
#### To do
- [ ] Ajuste detecção de voz.
- [ ] Redução de ruído.
- [x] Ajuste no loop de voz. Não fechar o programa quando acabar uma frase.
- [x] Comparação de texto para disparar uma ação.
- [ ] Docker.
- [x] Text to speech.
- [ ] Testes.
- [x] Integração com o KeyApp.
- [x] Envio do binário ao Cybervox. Atualmente é um aiff convertido para wav, gambiarra :see_no_evil:.
- [ ] NLP.
- [ ] Rasperry test.
- [ ] Adicionar Cyber wake up.
- [ ] Remover Jarvis como wake up word.
- [ ] Testar em Windows.

#### Pode ajudar:
Algumas referências que podem ajudar na pesquisa.
- https://github.com/amsehili/auditok
- https://core.ac.uk/download/pdf/230494941.pdf
- https://blog.appsumo.com/ultimate-guide-to-chatbots-2020/#decision
- https://cloud.google.com/dialogflow/docs/
- https://github.com/werman/noise-suppression-for-voice
- knowledge graph
- redes bayesianas
- decision trees