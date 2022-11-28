### Adding GCP Server to Teleport


#### Prerequisites

- Make sure you have access to gcloud servers locally i.e using [gcloud CLI](https://cloud.google.com/sdk/gcloud)
- Ensure you have sudo rights in the new server


#### Usage

* Get SSH configurations from `~/.ssh/config` for the new server and add them to `ssh.cfg`
    Sample SSH configs from `~/.ssh/config` file:
    ```
    Host agakhan-msa-db.europe-west1-b.speedy-lattice-334
        HostName 34.76.152.82
        IdentityFile <path-to-google-privake-key-file>
        UserKnownHostsFile=<path-to-google-known-hosts-file>
        HostKeyAlias=compute.1847378961746340905
        IdentitiesOnly=yes    
        CheckHostIP=no
    ```
* Give the server an appropriate name on `ssh.cfg`. Change the `Host` to an appropriate name.
***NOTE:*** The new name should be separated by an underscore:  `agakhan-msa-db` is INVALID, should be  `agakhan_msa_db`
* Test that the server can be accessed with the new configs by ssh-ing into the server with the new configs
	```bash	
    ssh -F ssh.cfg new_server_name
    ```
* Add the server name to group of teleport servers in `inventories/infrastructure/hosts/teleport_servers`
* Create a `new_server_name.yml` file in `inventories/infrastructure/host_vars` and add teleport configs for the new server.  
    * Sample teleport configs for a new provider server
    ```yaml
    teleport_proxy_address: "vault.slade360.co.ke:443"
    teleport_node_env: "prod" # 'testing' for test server
    teleport_node_site_type: "PROVIDER"
    teleport_node_location: "GCP"
    teleport_node_region: "Belgium"
    ```
    - `teleport_proxy_address` - address for proxy being used to access the server. 
       - For prod servers proxy address is `vault.slade360.co.ke:443`, for test servers, the proxy address is `mordor.slade360.co.ke:443`
    - `teleport_node_env` - Environment for the new server.   
       - For testing server, its value will be 'testing'
       - This is also used to manage roles in teleport.  
    - `teleport_node_site_type` - This describes the type of the new server. 
       - "PROVIDER" if the server will be used for provider applications, 'PAYER' if the server is used for payer applications
    - `teleport_node_location` - This describes where server is hosted. 
       - 'GCP' means the server is in Google Cloud Compute, 'EDGE' means the new server is on-premise
    - `teleport_node_region` - This is the physical location of the new server.
       - If the server is in GCP, its value will be the region of the server. For Edge servers, it will be location of the server e.g Mombasa

* FOR TELEPORT ADMINS:
	* Before running the playbook, get CA pin and token by running: 
     ```bash 
     sudo tctl tokens add --type=node
     ``` 
    * Sample output from the above command: 
    ```
    The invite token: 44f183dfe4e82100702c807c81e82ddf.
    This token will expire in 60 minutes.

    Run this on the new node to join the cluster:

    > teleport start \
       --roles=node \
       --token=44f183dfe4e82100702c807c81e82ddf \
       --ca-pin=sha256:961c70dd561c10fa039a77c41a10d4b4570187f92ed519b9224c5b0cc7cefcbd \
       --auth-server=10.240.0.48:3025

    Please note:

      - This invitation token will expire in 60 minutes
    ```

	* use the `CA pin` and` token value` for this playbook's input prompt:
*  Run this playbook `ansible-playbook -i inventories/infrastructure -l <new_server_name> -vvv teleport_node.yml`
* Change SSH configurations for the new server on `ssh.cfg` file to teleport-specific configurations
Final teleport-specific configuration:
    ```properties
    Host agakhan_msa_db
        HostName agakhan-mombasa-db
        Port 3022
        ProxyCommand ssh -p 3023 %r@vault.slade360.co.ke -s proxy:%h:%p
        UserKnownHostsFile=/dev/null
        HostkeyAlgorithms +ssh-rsa-cert-v01@openssh.com
        PubkeyAcceptedAlgorithms +ssh-rsa-cert-v01@openssh.com
    ```
    - `HOST` is the name of the new server as used in playbooks
    - `HOSTNAME` Is the name of the new server as registered in teleport.
    - `PORT` Is the SSH port used to connect to proxy
    - `ProxyCommand` Command used by teleport to forward connection to the new server
        - `3022` is the SSH port for teleport.
        - `3023` port is used by the new server when connecting to teleport
        - `%r@vault.slade360.co.ke` is the cluster for the new server when its a production server. For a testing server, this will be `%r@mordor.slade360.co.ke`

