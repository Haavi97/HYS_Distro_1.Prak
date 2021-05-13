#ReadME


## Failid
* MainNode.py - on websocket server, mis kuulab pordil 5000. Eesmärk on hallata IP aadressite listi, vajadusel lisada ning tagasi saata töödeldud listi. 
* IP_List.txt - IP aadressite list koos portidega, täpsemaid metaandmeid ei salvestata. 
* testCLI.py - Testimise eesmärgil loodud websocket client

## Märkmed
* Kui sissetulnud IP aadressit, ei ole olemasolevas listis, siis see sinna lisatakse. 
* Server eeldab et sissetulnud sõnum on alati IP aadress kujul "127.0.0.1:7000"
* Main node saadab alati vastu IP aadressite listi, kus ei ole sisse tulnud IP aadressi.
 
 * TestCLI on testimise eesmärgil loodud client. 
