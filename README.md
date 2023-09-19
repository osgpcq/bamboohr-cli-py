# bamboohr-cli-py
BambooHR Python command-line interface.

Extract informations from BambooHR.


# Usage
```
./bamboohr-cli.py --help
options:
  -h, --help           show this help message and exit
  --client CLIENT      Choose the credential (default: exo)
  --employees          List employees (default: False)
  --users              List users (default: False)
  --userenable         With --users only active one (default: False)
  --fields             List fields available for the company (default: False)
  --employee EMPLOYEE  Info for one employee ID (default: None)
  --whosout            Who is out (default: False)
  --today              With --whosout, who is out today (default: False)
  --timeoff TIMEOFF    iTimeoffCalculator need an employee ID (default: None)
  --noheaders          No headers in the output (default: False)
  --debug              Debug (default: False)
  --verbose            Verbose (default: False)

 ./bamboohr-cli.py --whosout --today
╭────┬───────┬─────────┬──────────────┬──────────────┬────────────┬────────────╮
│    │    id │ type    │   employeeId │ name         │ start      │ end        │
├────┼───────┼─────────┼──────────────┼──────────────┼────────────┼────────────┤
│  0 │ 13000 │ timeOff │          013 │ User1 User01 │ 2023-01-02 │ 2023-10-13 │
│  1 │ 13001 │ timeOff │          014 │ User2 User02 │ 2023-08-16 │ 2023-12-05 │
│  2 │ 13002 │ timeOff │          015 │ User3 User03 │ 2023-08-29 │ 2023-10-13 │
│  3 │ 13003 │ timeOff │          016 │ User4 User04 │ 2023-09-08 │ 2023-09-22 │

./bamboohr-cli.py --employees
╭────┬────┬──────────────┬───────────┬──────────┬────────────────┬───────────┬─────────────┬──────────────────┬────────────┬──────────┬──────────┬──────────┬───────────────╮
│    │ id │ displayName  │ firstName │ lastName │ preferredName  │ jobTitle  │   workPhone │ workEmail        │ department │ location │ division │ pronouns │ photoUploaded │
├────┼────┼──────────────┼───────────┼──────────┼────────────────┼───────────┼─────────────┼──────────────────┼────────────┼──────────┼──────────┼──────────┼───────────────┤
│  0 │ 13 │ User1 User01 │ User1     │ User01   │                │ COO       │             │ email@domain.ext │ Management │ Town     │ Company  │          │ True          │

./bamboohr-cli.py --employee 0
╭──────┬───────────┬──────────┬────────────╮
│   id │ firstName │ lastName │ hireDate   │
├──────┼───────────┼──────────┼────────────┤
│  287 │ User13    │ User013  │ 2019-03-04 │
╰──────┴───────────┴──────────┴────────────╯

./bamboohr-cli.py --timeoff 287
╭───────────────┬───────────────────┬─────────┬───────────┬────────────┬───────────────┬──────────────────╮
│   timeOffType │ name              │ units   │   balance │ end        │ policyType    │   usedYearToDate │
├───────────────┼───────────────────┼─────────┼───────────┼────────────┼───────────────┼──────────────────┤
│             1 │ Holidays          │ days    │        11 │ 2023-12-31 │ accruing      │             14   │
│             2 │ Birthday          │ days    │         1 │ 2023-12-31 │ accruing      │              0   │
│            17 │ Others leaves     │ hours   │         0 │ 2023-12-31 │ discretionary │             37.5 │
│            18 │ Telework          │ days    │         0 │ 2023-12-31 │ discretionary │              1   │
│             5 │ Compensation days │ days    │         0 │ 2023-12-31 │ discretionary │              0   │
╰───────────────┴───────────────────┴─────────┴───────────┴────────────┴───────────────┴──────────────────╯

./bamboohr-cli.py --users --userenable
╭─────┬──────┬──────────────┬───────────┬──────────┬──────────────────┬─────────┬───────────────────────────╮
│     │   id │   employeeId │ firstName │ lastName │ email            │ status  │ lastLogin                 │
├─────┼──────┼──────────────┼───────────┼──────────┼──────────────────┼─────────┼───────────────────────────┤
│   0 │ 1301 │           13 │ User1     │ User01   │ email@domain.ext │ enabled │ 2023-09-19T14:57:18+00:00 │
│   1 │ 1302 │           14 │ User2     │ User02   │ email@domain.ext │ enabled │ 2023-09-12T13:36:53+00:00 │
│   2 │ 1303 │           15 │ User3     │ User03   │ email@domain.ext │ enabled │ 2023-09-18T08:05:42+00:00 │

```


# History
Still in quick & dirty dev phase!
