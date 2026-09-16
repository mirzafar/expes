// Форматирование суммы в тенге: 1234.5 -> "1 234,50 ₸"
// Символ ₸ добавляем вручную — надёжнее, чем currency-режим (зависит от ICU среды)
const moneyFmt = new Intl.NumberFormat('ru-RU', {
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
})

export function formatMoney(amount) {
  return `${moneyFmt.format(amount ?? 0)} ₸`
}

// Дата ISO -> "16.09.2026"
const dateFmt = new Intl.DateTimeFormat('ru-RU', {
  day: '2-digit',
  month: '2-digit',
  year: 'numeric',
})

export function formatDate(iso) {
  if (!iso) return ''
  return dateFmt.format(new Date(iso))
}

// "2026-09" -> "Сен 26"
const MONTHS = ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек']
export function formatMonth(period) {
  if (!period) return ''
  const [year, month] = period.split('-')
  return `${MONTHS[Number(month) - 1]} ${year.slice(2)}`
}

// Короткая сумма для осей: 50000 -> "50к"
export function formatShort(n) {
  const abs = Math.abs(n)
  if (abs >= 1_000_000) return (n / 1_000_000).toFixed(1).replace('.0', '') + 'м'
  if (abs >= 1000) return (n / 1000).toFixed(1).replace('.0', '') + 'к'
  return String(n)
}
