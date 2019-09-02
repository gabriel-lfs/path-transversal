# Path Transversal

### Ariel Souza e Gabriel Souza

## Problema:
Primeiramente para ocasionar o erro expusemos 3 APIs:


* GET /files

Lista todos os arquivos na pasta raiz onde devem ser salvos os arquivos

* POST /upload_file

Envia arquivo para `files/api_uploaded_files` recebendo um json como corpo com os seguintes parâmetros:

```json
{
	"filename": "NomeDoArquivo.txt",
	"file": "RDo=" //base64 contendo o arquivo
}
```

* POST /download_file

Baixa arquivo de `files/api_uploaded_files` recebendo um json como corpo com os seguintes parâmetros:

```json
{
	"path": "nomeDoArquivo.txt"
}
```

A vunerabilidade pode ser explorada mandando no lugar do nome do arquivo nas duas apis um caminho alternativo

#### Download:
![](images/Screen Shot 2019-09-02 at 16.14.19.png)

#### Upload:
![](images/Screen Shot 2019-09-02 at 16.22.33.png)

* caso seja chamado o endpoint que lista os arquivos, ele não será enxergado pois está numa pasta acima da visualizada

![](images/Screen Shot 2019-09-02 at 16.14.00.png)

#### caminho:
![](images/Screen Shot 2019-09-02 at 16.22.52.png)

## Como resolvemos o problema:

Foi criado um novo projeto em que quando um arquivo é uploadado, um UUID é atribuido a ele independente de seu nome

![](images/Screen Shot 2019-09-02 at 17.12.16.png)

![](images/Screen Shot 2019-09-02 at 17.12.55.png)

logo, não é mais possível de fazer a injeção pois caso tentemos buscar o arquivo utilizando wildcards no path do sistema sempre será gravado um UUID

E caso tentemos acessar um arqivo fora do escopo, no caso, que não esta cadastrado na base, nada será retornado.

![](images/Screen Shot 2019-09-02 at 17.13.28.png)