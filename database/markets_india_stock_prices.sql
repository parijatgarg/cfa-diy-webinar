CREATE TABLE `markets_india_stock_prices` (
  `instrument_id` int(11) NOT NULL,
  `trade_date` date DEFAULT NULL,
  `open` float DEFAULT NULL,
  `high` float DEFAULT NULL,
  `low` float DEFAULT NULL,
  `close` float DEFAULT NULL,
  `last_price` float DEFAULT NULL,
  `traded_volume` int(11) DEFAULT NULL,
  `traded_value` float DEFAULT NULL,
  UNIQUE KEY `uniquerecord` (`instrument_id`,`trade_date`),
  KEY `instrument_based_index` (`instrument_id`),
  KEY `date_based_index` (`trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;