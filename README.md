# InfluxDB Integration Pack

This pack interfaces with the [InfluxDB](https://www.influxdata.com/time-series-platform/influxdb/) REST [API](https://docs.influxdata.com/influxdb/latest/tools/api).
Actions are available to both query for and write data to an InfluxDB instance.
This pack utilizes InfluxDB terminology, for more information we suggest reviewing
the [key concepts](https://docs.influxdata.com/influxdb/latest/concepts/key_concepts/)
and the [glossery of terms](https://docs.influxdata.com/influxdb/latest/concepts/glossary/).

## Configuration

Copy the example configuration in [influxdb.yaml.example](./influxdb.yaml.example)
to `/opt/stackstorm/configs/influxdb.yaml` and edit as required.

* `server` - The hostname/IP of the default InfluxDB server.
* `port` - Port number to connect to InfluxDB on (default: 8086)
* `ssl` - Use SSL/HTTPS
* `verify_ssl` - Verify remote host SSL certificates
* `credentials` - Mapping of name to an object containing credential information
  * `username` - User to authenticate as
  * `password` - Password to authenticate with.

**Note** : All actions allow you to specify a `credentials` parameter that will
           reference the `credentials` information in the config. Alternatively
           all actions allow you to override these credential parameters so a
           config isn't required.

**Note** : When modifying the configuration in `/opt/stackstorm/configs/` please
           remember to tell StackStorm to load these new values by running
           `st2ctl reload --register-configs`

### Configuration Credentials

Most options in the config are simply key/value pairs, with the exception of `credentials`.
In order to make working with the InfluxDB pack easier, we've provided a mechanism to
store credentials in the pack's config. Credentials are stored as a dictionary, sometimes
called a hash, where the key is the name of the credential and the values are 
the credential information (username, password, etc).

Below is an example of a simple config with a single credential named `dev`:

``` yaml
credentials:
  dev:
    username: 'test_user'
    password: 'myPassword'
```

Multiple credentials can also be specified:

``` yaml
credentials:
  dev:
    username: 'test_user'
    password: 'myPassword'
  qa:
    username: 'qa_user'
    password: 'xxxYYYzzz!!!'
  prod:
    username: 'prod_user'
    password: 'lkdjfldsfjO#U)R$'
```

These credentials can then be referenced by name when executing a `influxdb` pack action
using the `credentials` parameter available on every action. Example:

``` shell
# use login information from the "dev" credential stored in the config
st2 run influxdb.query query="select * from my_measurement" server="influxdb.domain.tld" credentials="dev"
```

### Configuration Credentials - Default

If a credential parameter is not specified, then we will attempt to lookup a credential
with the name of `default`. This allows end users to specify a default set of credentials
to be used via the config.

Example config:
``` yaml
credentials:
  default:
    username: 'default_user'
    password: 'abc123'
```

Example command using default credentials

``` shell
# use login information from the "default" credential stored in the config because
# the credentials parameter was not pass in
st2 run influxdb.query query="select * from my_measurement" server="influxdb.domain.tld"
```

### Configuration Example

The configuration below is an example of what a end-user config might look like.
One of the most common config options will most likely be the `modulepath`, that will
direct `bolt` at the place where they've installed their Puppet modules.

``` yaml
---
server: influxdb.domain.tld
port: 443
ssl: true
verify_ssl: true

credentials:
  default:
    username: 'myuser'
    password: 'secretSauce!'
```


# Actions

* `ping` - Use this endpoint to check the status of your InfluxDB instance and your version of InfluxDB. [/ping](https://docs.influxdata.com/influxdb/latest/tools/api/#ping-http-endpoint)
* `query` - Query data and manage databases,retention policies and users. [/query](https://docs.influxdata.com/influxdb/latest/tools/api/#query-string-parameters-1)
* `write` - Use this endpoint to write data to a pre-existing database. [/write](https://docs.influxdata.com/influxdb/latest/tools/api/#write-http-endpoint)

## Action Example - ping

Ping a InfluxDB instance and check its status and version.

``` shell
$ st2 run influxdb.ping server=influxdb.domain.tld
.
id: 5bc7dfb69387ef0673b72741
status: succeeded
parameters: 
  server: influxdb.domain.tld
result: 
  exit_code: 0
  result: 1.6.4
  stderr: ''
  stdout: ''
```

## Action Example - query

Run an arbitrary query using the [InfluxQL](https://docs.influxdata.com/influxdb/latest/query_language/)
syntax.

``` shell
$ st2 run influxdb.query query="show databases" server=influxdb.domain.tld
id: 5bc7eb9f9387ef0673b72754
status: succeeded
parameters: 
  query: show databases
  server: influxdb.domain.tld
result: 
  exit_code: 0
  result:
  - series:
    - columns:
      - name
      name: databases
      values:
      - - _internal
      - - exampledb
    statement_id: 0
  stderr: ''
  stdout: ''

```

## Action Example - write

Writes data into an InfluxDB database `measurement`.
The data can be passed in one of two ways:
* Using navive arrays and object in the `points` paramter
* Using a raw string where data is in the [Line Protocol Format](https://docs.influxdata.com/influxdb/latest/concepts/glossary/#line-protocol) in the `points_raw` parameter.

## Action Example - write points

When writing data into InfluxDB from StackStorm, the logical way to do this is using
native arrays and objects within StackStorm. To do this pass an array of objects
to the `points` parameter. This array of objects should have the following schema:

```yaml
points:
  type: array
  items:
    type: object
    paramters:
      measurement:
        type: string
        description:
          Name of the measurement
      tags:
        type: object
        description:
          Object containing tags where the key is the tag name and the value
          is the tag value.
      time:
        type: string OR integer
        description:
          Can either be the timestamp string (ISO format) or an integer
          containing the epoch time.
      fields:
        type: object
        description:
          Object containing field values where the field name is the key
          and the value is the data.
```

Example points array (YAML):

``` yaml
- measurement: "meas"
  tags:
    tag1: "t1"
  time: 1234
  fields: 
    value: 43
```

Example points array (JSON):

``` json
[
    {
        "measurement": "meas", 
        "tags": 
        {
            "tag1": "t1"
        }, 
        "time": 1234, 
        "fields": 
        {
            "value": 43
        }
    }
]
```

Example of using the `points` parameter:

``` shell
$ st2 run influxdb.write points='[{"measurement": "meas", "tags": {"tag1": "t1"}, "time": 1234, "fields": {"value": 43}}]' database=exampledb server=influxdb.domain.tld
.
id: 5bc7e67a9387ef0673b7274e
status: succeeded
parameters: 
  database: exampledb
  points:
  - fields:
      value: 43
    measurement: meas
    tags:
      tag1: t1
    time: 1234
  server: influxdb.domain.tld
result: 
  exit_code: 0
  result: true
  stderr: ''
  stdout: ''

```

## Action Example - write points_raw

Alternatively you can create a string with raw data points, encoded in the InfluxDB
[Line Protocol Format](https://docs.influxdata.com/influxdb/latest/concepts/glossary/#line-protocol).
To utilize this raw format, pass your string into the in the `points_raw` parameter.


Example Line Protocol Format points:
``` shell
meas,tag1=t1 value=43i 1234
```

Example writing points using the raw Line Protocol Format:

``` shell
$ st2 run influxdb.write points_raw="meas,tag1=t1 value=43i 1234" database=exampledb server=influxdb.domain.tld
.
id: 5bc7f2069387ef0673b72784
status: succeeded
parameters: 
  database: exampledb
  points_raw: meas,tag1=t1 value=43i 1235
  server: influxdb.domain.tld
result: 
  exit_code: 0
  result: true
  stderr: ''
  stdout: ''
```
