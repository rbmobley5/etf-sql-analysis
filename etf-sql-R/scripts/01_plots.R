########## Normalized index price #######################
normalized <- prices %>%
  group_by(ticker) %>%
  arrange(date) %>%
  mutate(indexed = close / first(close) * 100)

p1 <- ggplot(normalized, aes(x = date, y = indexed, color = ticker)) +
  geom_line(linewidth = 0.8) +
  labs(
    title = "Vanguard ETF Performance (Indexed to 100)",
    subtitle = "VTI, VOO, BND — January 2021 to December 2024",
    x = NULL, y = "Indexed Price", color = NULL
  ) +
  scale_color_manual(values = c("VTI" = "#185FA5", "VOO" = "#1D9E75", "BND" = "#D85A30")) +
  theme_minimal(base_size = 12)

p1
ggsave("figures/indexed_performance.png", p1, width = 8, height = 4.5, dpi = 150)

################### Volatility #########################################
volatility <- prices %>%
  group_by(ticker) %>%
  arrange(date) %>%
  mutate(
    daily_return = (close - lag(close)) / lag(close),
    vol_30d = rollapply(daily_return, 30, sd, fill = NA, align = "right") * sqrt(252) * 100
  )

p2 <- ggplot(volatility, aes(x = date, y = vol_30d, color = ticker)) +
  geom_line(linewidth = 0.7, alpha = 0.85) +
  labs(
    title = "Annualized 30-Day Rolling Volatility",
    subtitle = "Higher = more price swings day to day",
    x = NULL, y = "Volatility (%)", color = NULL
  ) +
  scale_color_manual(values = c("VTI" = "#185FA5", "VOO" = "#1D9E75", "BND" = "#D85A30")) +
  theme_minimal(base_size = 12)

p2
ggsave("figures/rolling_volatility.png", p2, width = 8, height = 4.5, dpi = 150)


####### Annual Returns ########
annual <- prices %>%
  group_by(ticker, year = year(date)) %>%
  summarise(
    annual_return = (last(close) - first(close)) / first(close) * 100,
    .groups = "drop"
  )

p3 <- ggplot(annual, aes(x = factor(year), y = annual_return, fill = ticker)) +
  geom_col(position = "dodge") +
  geom_hline(yintercept = 0, linewidth = 0.4) +
  labs(
    title = "Annual Returns by ETF",
    subtitle = "VTI, VOO, BND — 2021 to 2024",
    x = NULL, y = "Return (%)", fill = NULL
  ) +
  scale_fill_manual(values = c("VTI" = "#185FA5", "VOO" = "#1D9E75", "BND" = "#D85A30")) +
  theme_minimal(base_size = 12)

p3
ggsave("figures/annual_returns.png", p3, width = 8, height = 4.5, dpi = 150)
