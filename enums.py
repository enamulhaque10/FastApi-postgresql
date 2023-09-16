from enum import Enum, unique


class ProductTags(str, Enum):
  LATEST = "LATEST"
  NEW = "NEW"
  MOST_VIEW  = "MOST_VIEW" 

class ActiveStatus(str, Enum):
  ACTIVE = "ACTIVE"
  DEACTIVE = "DEACTIVE"