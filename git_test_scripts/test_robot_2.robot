#Filename of .py and class name inside that .py file should be same
| *** Settings *** |
| Documentation  | Validate Hook PSU FW update feature with config: 2+0 / 1+1, Sled Power: On / Off, PSU PGood: 0 / 1  |

| Library        | PSU_FW_Update.py |

| *** Variables *** |
| ${SERIAL_PORT}    | COM11 |
#| ${CYCLES}    | 1 |

# Variables for internal use only, Do not change
| ${DOWNGRADE_RET} | ${EMPTY} |
| ${UPGRADE_RET} | ${EMPTY} |
| ${TEST_RET} | ${EMPTY} |

| *** Test Cases *** |

| TEST_1 |
|    | [ Tags ] | TEST_ONE |
|    | @{output} = | pqrs | ${SERIAL_PORT} | 
# |    | Run Keyword If  | '${TEST_RET[0]}' == 'FAIL' | FAIL |
|    | Set Global Variable | @{output} |


| TEST_2 |
|    | [ Tags ] | TEST_TWO |
|    | ${UPGRADE_RET}= | abcd | ${output[1]} | 
|    | Run Keyword If  | '${UPGRADE_RET}' == 'FAIL' | FAIL |


# | *** Keywords *** |

# | pqrs_test |
# |    | [Arguments] | ${arg_0} |  
# |    | @{iRet}=   | PSU_FW_Update.pqrs | ${arg_0} | 
# |    | [Return]    | @{iRet} |

# | abcd_test |
# |    | [Arguments] | ${arg_0} |  
# |    | ${iRet} =   | PSU_FW_Update.abcd | ${arg_0} | 
# |    | [Return]    | ${iRet} |