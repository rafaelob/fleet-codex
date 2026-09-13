# Arranjos de agentes para Codex

Este catálogo reúne combinações completas de um agente principal e seus
especialistas. Os arquivos funcionam sem framework privado, servidor MCP ou
skills externas obrigatórias. Cada arranjo fornece 19 papéis; você inicia apenas
os que ajudam na tarefa.

| Arranjo | Principal | Especialistas |
| --- | --- | --- |
| [Advanced Delivery](../arrangements/advanced-delivery/README.md) | Sol `xhigh` | 4 Astra, 9 Terra e 6 Luna |
| [Lean Delivery](../arrangements/lean-delivery/README.md) | Sol `high` | 1 Astra, 1 Sol e 17 Luna |

Ambos habilitam Multi-Agent V2. Advanced Delivery prioriza trabalhos de produto
complexos, com mais modelos fortes para decisões e implementação acoplada.
Lean Delivery prioriza o custo em trabalho bem definido, concentra trabalho em Luna e reserva
Sol `high` para revisão da integração e Astra para revisão crítica.
Frontend e backend ficam com Luna, assim como os demais papéis.
Isso descreve a distribuição escolhida; não é uma promessa medida de preço ou
qualidade. Os tetos configurados são 6 e 7, com recomendação conservadora de até
5 e 6 filhos ativos, respectivamente. Confira a [compatibilidade](validation.md).

## Instalar

1. Tenha o Codex autenticado e confira `codex --version` e seu acesso aos modelos.
   Baixe uma revisão conferida deste catálogo e escolha um arranjo.
2. Escolha o nível: usuário (`$CODEX_HOME`, normalmente `~/.codex`) ou projeto
   (`<projeto>/.codex`). Salve uma cópia local dos arquivos que editará.
3. Mescle o fragmento `config.toml` nos blocos existentes. Não duplique tabelas
   TOML nem substitua o arquivo inteiro. Copie os TOMLs para `agents/` nesse nível,
   conferindo colisões de nomes antes de substituir arquivos.
4. Insira `AGENTS.snippet.md` no AGENTS.md do usuário ou na raiz do projeto.
   Preserve as demais instruções e confira se existe um AGENTS.override.md ativo.
5. Abra uma nova sessão e confirme os papéis e configurações carregados. Projeto
   precisa ser confiável para carregar suas configurações e hooks.

Opcionalmente, copie `skills/codex-orchestration` e/ou `skills/pragmatic-programmer`,
cada uma inteira com licença e aviso, para `~/.agents/skills/` ou
`<projeto>/.agents/skills/`. Nesse caso use `AGENTS.with-skill.snippet.md` em lugar
do outro trecho. Ele chama `$codex-orchestration` ao delegar e
`$pragmatic-programmer` nas decisões de projeto, resultados sem causa explicada,
duplicação de conhecimento, estado compartilhado e recursos finitos. Cada chamada
fica junto da situação que a justifica, com orientação quando a skill não existe.
As seções são independentes: se não instalar Pragmatic Programmer, omita sua
seção opcional. As regras pedem a ferramenta de skills pelo nome exato quando
ela existe; caso contrário, usam o mecanismo nativo de carregamento do runtime,
sem inventar uma API `Skill`.

As [skills](../skills/README.md) ficam fora dos arranjos e podem servir outros
fluxos. A área de [plugins](../plugins/README.md) também recebe contribuições
independentes no formato oficial, que podem reunir skills, MCP e hooks. Esta
primeira versão não inclui um plugin instalável; escolher um arranjo não instala
nem ativa essas integrações opcionais.

O [hook opcional](../hooks/spawn-contract/README.md) exige Python 3.11+, caminhos
locais ajustados e confiança na definição exata pelo `/hooks`. Ele verifica papel
explícito, `fork_turns: "none"` e ausência de override de modelo/esforço. Sua
cobertura depende da versão do runtime; não promete impedir recursão.

As permissões, credenciais e ferramentas do seu ambiente continuam sendo suas.
Subagentes podem herdá-las. Não copie sua configuração pessoal inteira para uma
contribuição pública.

## Verificar e contribuir

Do diretório do catálogo, execute:

```text
python -X utf8 scripts/validate_catalog.py
python -X utf8 scripts/validate_components.py
python -X utf8 -m unittest discover -s tests -v
```

Em um projeto descartável, peça uma exploração, uma pequena implementação
autorizada e uma revisão independente. Confira artefatos e registros reais de
modelo e esforço. Testes do script não provam que o Codex chamou o hook.

Para remover, apague apenas os componentes instalados e reverta os campos que
você alterou, preservando suas mudanças posteriores. Reinicie o Codex.

O [guia completo](installation.md) explica precedência, atualização e reversão.
Para compartilhar outra combinação, siga [CONTRIBUTING.md](../CONTRIBUTING.md)
e envie um PR com os TOMLs, a justificativa, a licença e evidências sanitizadas.
Use inglês nos arquivos instaláveis, Issues e PRs. Guias complementares, como
este, podem ser traduzidos. Você também pode propor correções em arranjos
existentes usando o formulário de correção do repositório.
