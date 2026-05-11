import json
from pathlib import Path


OUTPUT_FILE = Path("data/manual_fragments.jsonl")

FRAGMENTS = [
    {
        "id": 1,
        "title": "Cadeia de custódia digital",
        "text": "A cadeia de custódia digital consiste no registro formal, cronológico e verificável de todas as etapas de coleta, transporte, armazenamento, análise e apresentação da evidência digital, garantindo autenticidade, integridade e rastreabilidade."
    },
    {
        "id": 2,
        "title": "Aquisição forense bit a bit",
        "text": "A aquisição forense bit a bit corresponde à criação de uma cópia integral do dispositivo de armazenamento, incluindo espaço não alocado, setores marcados como excluídos e metadados do sistema de arquivos, preservando o estado original da evidência."
    },
    {
        "id": 3,
        "title": "Função hash na verificação de integridade",
        "text": "Funções hash criptográficas, como SHA-256, são utilizadas para verificar a integridade de evidências digitais, permitindo comprovar que o arquivo ou imagem forense não sofreu alteração entre a coleta e a análise."
    },
    {
        "id": 4,
        "title": "Artefatos de sistema operacional",
        "text": "Artefatos de sistema operacional incluem logs, arquivos temporários, registros de eventos, histórico de execução e metadados que podem indicar uso de programas, conexão de dispositivos externos e alterações realizadas no ambiente computacional."
    },
    {
        "id": 5,
        "title": "Análise de timestamps",
        "text": "A análise de timestamps envolve a correlação de datas e horários de criação, modificação, acesso e mudança de metadados, sendo essencial para reconstruir a linha temporal dos eventos em uma investigação pericial."
    },
    {
        "id": 6,
        "title": "Espaço não alocado",
        "text": "O espaço não alocado pode conter fragmentos de arquivos apagados logicamente, permitindo a recuperação parcial ou total de evidências que não estejam mais visíveis ao usuário no sistema operacional."
    },
    {
        "id": 7,
        "title": "Recuperação de arquivos excluídos",
        "text": "A recuperação de arquivos excluídos depende do estado do sistema de arquivos, da sobrescrita de blocos e da preservação dos metadados. A simples exclusão lógica não implica remoção imediata do conteúdo do disco."
    },
    {
        "id": 8,
        "title": "Memória volátil",
        "text": "A memória volátil pode armazenar credenciais temporárias, processos em execução, conexões de rede, chaves criptográficas e artefatos de execução recente. Sua coleta deve ser priorizada antes do desligamento do equipamento."
    },
    {
        "id": 9,
        "title": "Imagem forense",
        "text": "Uma imagem forense é uma representação fiel do conteúdo de um meio digital, produzida com ferramentas apropriadas e acompanhada de verificação de integridade para permitir análise sem alteração do material original."
    },
    {
        "id": 10,
        "title": "Metadados de arquivos",
        "text": "Metadados de arquivos podem incluir autor, datas, permissões, localização, software de origem e histórico de modificação, sendo úteis para contextualização da evidência e identificação de manipulações."
    },
    {
        "id": 11,
        "title": "Registro de dispositivos USB",
        "text": "Vestígios de conexão de dispositivos USB podem ser encontrados em artefatos do sistema operacional, permitindo inferir quando determinado pendrive foi conectado, qual identificador de hardware estava presente e, em alguns casos, qual usuário estava ativo."
    },
    {
        "id": 12,
        "title": "Logs de autenticação",
        "text": "Logs de autenticação registram tentativas de login, falhas, bloqueios, horários e origens de acesso. Esses registros são relevantes para identificar uso indevido de contas e movimentação lateral em ambientes corporativos."
    },
    {
        "id": 13,
        "title": "Correlação temporal de eventos",
        "text": "A correlação temporal de eventos consiste em comparar artefatos de múltiplas fontes, como sistema operacional, firewall, proxy e aplicação, para reconstruir a sequência provável das ações executadas."
    },
    {
        "id": 14,
        "title": "Análise de evidência em rede",
        "text": "A evidência em rede pode incluir pacotes capturados, registros de firewall, DNS, proxy e roteadores. Esses elementos auxiliam na identificação de comunicação suspeita, exfiltração de dados e conexões com serviços externos."
    },
    {
        "id": 15,
        "title": "Preservação da evidência",
        "text": "A preservação da evidência digital exige isolamento do dispositivo, documentação detalhada, uso de bloqueadores de escrita quando aplicável e registro formal de todas as intervenções técnicas realizadas."
    },
    {
        "id": 16,
        "title": "Documentação pericial",
        "text": "A documentação pericial deve descrever ferramentas utilizadas, procedimentos executados, resultados obtidos, limitações encontradas e fundamentos técnicos que sustentam as conclusões do exame."
    },
    {
        "id": 17,
        "title": "Análise de histórico de navegação",
        "text": "O histórico de navegação pode conter URLs visitadas, datas, horários, pesquisas realizadas, sessões autenticadas e indicadores de interação com serviços web, sendo útil em exames de atividade do usuário."
    },
    {
        "id": 18,
        "title": "Persistência de malware",
        "text": "Mecanismos de persistência de malware podem envolver chaves de inicialização, tarefas agendadas, serviços, alterações em registro e modificações em scripts de boot, mantendo a execução maliciosa após reinicializações."
    },
    {
        "id": 19,
        "title": "Análise de e-mails",
        "text": "A análise de e-mails considera cabeçalhos, remetentes, rotas de entrega, anexos, links incorporados e metadados da mensagem, permitindo investigar fraude, phishing e circulação de informação sensível."
    },
    {
        "id": 20,
        "title": "Autenticidade de imagens digitais",
        "text": "A autenticidade de imagens digitais pode ser investigada por meio de metadados EXIF, inconsistências de compressão, análise de edição, comparação de hashes e correlação com contexto temporal e de origem."
    },
    {
        "id": 21,
        "title": "Análise de sistemas de arquivos",
        "text": "A análise de sistemas de arquivos examina estruturas lógicas como MFT, inodes, diretórios, journals e mapas de alocação, permitindo localizar evidências persistentes, excluídas ou parcialmente corrompidas."
    },
    {
        "id": 22,
        "title": "Boas práticas de coleta em dispositivos móveis",
        "text": "A coleta em dispositivos móveis deve considerar modo avião, isolamento de rede, estado de bloqueio, risco de sincronização remota e preservação do conteúdo local e em nuvem associado ao aparelho."
    },
    {
        "id": 23,
        "title": "Análise de logs de aplicativos",
        "text": "Logs de aplicativos podem registrar autenticações, falhas, ações de usuário, erros de execução e mudanças de configuração, sendo úteis para reconstruir eventos e identificar comportamento anômalo em sistemas corporativos."
    },
    {
        "id": 24,
        "title": "Bloqueadores de escrita",
        "text": "Bloqueadores de escrita são dispositivos ou mecanismos utilizados para impedir alterações no meio original durante a aquisição forense, preservando a integridade da evidência e reduzindo o risco de contaminação do material analisado."
    },
    {
        "id": 25,
        "title": "Correlação entre evidência local e evidência em nuvem",
        "text": "A correlação entre evidência local e evidência em nuvem permite verificar sincronização de arquivos, histórico de acesso, alterações remotas e movimentação de dados entre dispositivos e serviços externos, ampliando a reconstrução dos fatos investigados."
    }
]


def save_jsonl(file_path: Path, records: list[dict]) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


def main() -> None:
    
    save_jsonl(OUTPUT_FILE, FRAGMENTS)

    print(f"Total de fragmentos: {len(FRAGMENTS)}")
    print(f"Arquivo salvo em: {OUTPUT_FILE.resolve()}")


if __name__ == "__main__":
    main()