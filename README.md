# Project Whites Test

## Overview

The project is built on Odoo 15 Community Edition. This project includes several modules :
- Whites PoS (PoS Refund Authorization)
- Whites Report (Sales Report with SQL Pivot)
- Whites Account (Mandatory Analytic Account & Partner Validation)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ivanoctaviano/whites-test
   cd whites-test
   ```

2. **Install Odoo**
Build Odoo 15 CE service by execute docker-compose file

```bash
  docker-compose up -d
```

Use this command to check if all services are running well

```bash
  docker ps
```

## Usage

### PoS Refund Authorization

#### Description

This module customizes PoS to prompt password before proceeding to Refund Process. The password is need to be set on Employee Profile.

#### Demo
[Watch the demo video][https://www.loom.com/share/868d5254c4f44f3a886f028cc92894d2]

### Sales Report with SQL Pivot

#### Description

This module generates a SQL-based pivot report that consolidates data from Sales Orders and POS Orders into a single structured report.

#### Demo
[Watch the demo video][https://www.loom.com/share/8cfbfe25590f4a849077c44922a6200c]

### Mandatory Analytic Account & Partner Validation

#### Description

This module modifies the Chart of Accounts to introduce restrictions on specific accounts that require an analytic account and a partner.

#### Demo
[Watch the demo video][https://www.loom.com/share/f712fe95aa364c5ca2eae814979728bf]