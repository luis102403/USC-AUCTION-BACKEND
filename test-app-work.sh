# BUILD APP

sam build --template-file template.test.yaml

# START APP

sam local start-api -p 8080 --docker-network 675bb0c6b350  --log-file logs.txt
