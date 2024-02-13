# wazuh-agent-kubernetes-operator
Kubernetes Operator for deployment Wazuh Agent for any Kubernetes platform.

## Disclaimer
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


## How to deploy operator

Apply Kubernetes manifests for [CR](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/)

```shell
kubectl apply -f crd/operator.yml
```

Apply deployment for operator

```shell
kubectl apply -f crd/deployment.yml

```

## Creation of Custom resource

Before creation of CRD for operator please take a look current schema:

| name              | type   | description                                                                                                                                                      | default value         | optional |   |   |
|-------------------|--------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------|----------|---|---|
| `name`            | string | All resources within a release are prefixed based on the name                                                                                                    | `opn`                 | `true`   |   |   |
| `image_url`       | string | Docker image url for pulling wazuh agent                                                                                                                         | `opennix/wazuh-agent` | `true`   |   |   |
| `image_tag`       | string | Wazuh agent docker image tag                                                                                                                                     | `latest`              | `true`   |   |   |
| `manager_host`    | string | IP address or domain name of the Wazuh server used for REST API calls.                                                                                           | `localhost`           | `false`  |   |   |
| `worker_host`     | string | The IP address or domain name of the Wazuh worker for agent connection should be provided. If using an ALL-in-One installation, this field should be left empty. | `None`                | `true`   |   |   |
| `api_username`    | string | Username for Wazuh API authorization                                                                                                                             | `None`                | `true`   |   |   |
| `api_password`    | string | Password for Wazuh API autorization	                                                                                                                             | `None`                | `false`  |   |   |
| `group`           | string | Group name(s), separated by commas, for automatically adding agents.                                                                                             | `default`             | `true`   |   |   |
| `memory_limits`   | string | Memory limit for agent container                                                                                                                                 | `128Mi`               | true     |   |   |
| `cpu_limits`      | string | Cpu limit for agent container                                                                                                                                    | `128m`                | true     |   |   |
| `memory_requests` | string | Memory request for agent container                                                                                                                               | `64Mi`                | true     |   |   |
| `cpu_requests`    | string | Cpu request for agent container                                                                                                                                  | `64m`                 | true     |   |   |

Example of crd is available in path `deployments/example.yml`



<a href="https://www.buymeacoffee.com/pyToshka" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>
