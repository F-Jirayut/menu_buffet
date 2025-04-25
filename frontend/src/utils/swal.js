import Swal from 'sweetalert2'

export const showSuccess = (title = 'สำเร็จ', text = '', timer = 1500) => {
  return Swal.fire({
    icon: 'success',
    title,
    text,
    timer: timer,
    showConfirmButton: false,
  })
}

export const showSuccessOk = (title = 'สำเร็จ', text = '', confirmButtonText = 'ตกลง')=> {
  return Swal.fire({
    icon: 'success',
    title,
    text,
    confirmButtonText,
  })
}

export const showError = (title = 'เกิดข้อผิดพลาด', text = '') => {
  return Swal.fire({
    icon: 'error',
    title,
    text,
    confirmButtonText: 'ตกลง',
  })
}

export const showLoading = (title = 'กำลังโหลด...') => {
  return Swal.fire({
    title,
    allowOutsideClick: false,
    didOpen: () => {
      Swal.showLoading()
    },
  })
}

export const closeSwal = () => {
  Swal.close()
}

export const showConfirm = (
  title = 'คุณแน่ใจหรือไม่?',
  text = 'คุณไม่สามารถย้อนกลับได้!',
  confirmButtonText = 'ยืนยัน',
  cancelButtonText = 'ยกเลิก'
) => {
  return Swal.fire({
    title,
    text,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#d33',
    cancelButtonColor: '#3085d6',
    confirmButtonText,
    cancelButtonText,
  })
}

