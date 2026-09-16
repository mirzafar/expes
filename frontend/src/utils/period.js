// Периоды для фильтрации. По умолчанию везде — текущий месяц.
export const PERIODS = [
  { key: 'month', label: 'Этот месяц' },
  { key: 'prev', label: 'Прошлый месяц' },
  { key: 'all', label: 'Всё время' },
]

export const DEFAULT_PERIOD = 'month'

// Возвращает { date_from, date_to } в ISO для заданного периода.
// Для 'all' — пустой объект (без ограничений).
export function periodRange(key) {
  if (key === 'all') return {}

  const now = new Date()
  let year = now.getFullYear()
  let month = now.getMonth() // 0..11

  if (key === 'prev') {
    month -= 1
    if (month < 0) {
      month = 11
      year -= 1
    }
  }

  const from = new Date(year, month, 1, 0, 0, 0, 0)
  const to = new Date(year, month + 1, 0, 23, 59, 59, 999) // последний день месяца
  return { date_from: from.toISOString(), date_to: to.toISOString() }
}
