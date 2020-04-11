CREATE TABLE `markets_india_stock_symbols` (
  `instrument_id` int(11) NOT NULL AUTO_INCREMENT,
  `nse` char(10) DEFAULT NULL,
  `bse` char(10) DEFAULT NULL,
  `isin` char(12) DEFAULT NULL,
  `cin` char(21) DEFAULT NULL,
  `paidup_value` float DEFAULT NULL,
  `industry` varchar(40) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`instrument_id`),
  KEY `nse_instrument_index` (`nse`,`instrument_id`),
  KEY `bse_instrument_index` (`bse`,`instrument_id`),
  KEY `isin_instrument_index` (`isin`,`instrument_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;