# Configurações
Estão contidas no arquivo dhcp_config.json

#Rodar
sudo python dhcp_spoof.py

#Detalhes HTTP - TO DO list:
- Algumas requisições podem estar duplicadas por causa de cookies fragmentados
- Filtrar ida e volta (porta origem, porta destino)
    + Ao chegar um pacote válido recebido, guardar em memória
    + Ao receber um pacote http, bater com o q foi guardado na memória
        * Se existir porta-origem,ip verificar se content/type for html
            - Se não for html, remove do mapa
                + def removekey(d, key):
                    r = dict(d)
                    del r[key]
                    return r