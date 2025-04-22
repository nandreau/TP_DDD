import { useToast } from 'primevue/usetoast'

let _toast

export function initToast() {
  _toast = useToast()
}

export function getToast() {
  return _toast
}