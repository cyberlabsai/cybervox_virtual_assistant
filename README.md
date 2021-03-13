### Cybervox Virtual Assistant
Pérola é o primeiro projeto Opensource brasileiro de assistente virtual. Ela ainda é um bebê que está aprendendo a engatinhar. Contribua com o seu desenvolvimento.

#### Start
##### Create enviroment and actions
```
    cp .env.example .env && cp actions.example.json actions.json
```
###### Exec
```
    python app.py
```
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

#### Pode ajudar:
- https://github.com/amsehili/auditok
- knowledge graph
- redes bayesianas
- decision trees
- https://core.ac.uk/download/pdf/230494941.pdf
- https://blog.appsumo.com/ultimate-guide-to-chatbots-2020/#decision