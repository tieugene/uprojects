| [TOC](TOC.md) | [Server](Inst_S.md) |
|:--------------|:--------------------|

# Introduction #

This manual is for implementing LDAP-based LAN, based on CentOS 6.0.

## Objects: ##

  * users
  * hosts
  * resources

## Structure: ##

  * packages
  * deps
  * configs and data
  * installation
  * setting up
  * check
  * deleting
  * controlling of objects:
    * add
    * delete
    * change
  * backup/restore
    * configs
    * data
  * migration (to another host)
    * network
    * server name
    * domain
## Source data: ##
  * LAN:
| Net | 192.168.0.0/24 |
|:----|:---------------|
| Server | 192.168.0.1    |
| X-terminal server | 192.168.0.2    |
| other hosts | host002..host253 |
| GW  | 192.168.0.254  |
| domain | lan.           |

  * LDAP:
| root | dc=ldap |
|:-----|:--------|
| odmin | cn=odmin,dc=ldap |
| password | secred  |

  * extranet
| domain | example.com |
|:-------|:------------|

  * Users
    * user00 (uid=500)..userXX (uid=5XX)
    * group00 (gid=500)..groupYY (gid=5XX)
  * Samba:
| domain | WINDOMAIN |
|:-------|:----------|