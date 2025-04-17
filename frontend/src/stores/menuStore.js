import { defineStore } from 'pinia'

export const useMenuStore = defineStore('menu', {
  state: () => ({
    items: [
        {
            name: 'ข้าวผัดหมู',
            description: 'ข้าวผัดหมูหอมๆ เสิร์ฟพร้อมแตงกวาและมะนาว',
            price: 50,
            image: 'https://dummyimage.com/400x300'
          },
          {
            name: 'ผัดไทยกุ้งสด',
            description: 'ผัดไทยเส้นเหนียวนุ่มพร้อมกุ้งสดตัวใหญ่',
            price: 60,
            image: 'https://dummyimage.com/400x300'
          },
          {
            name: 'ต้มยำกุ้ง',
            description: 'ต้มยำกุ้งรสจัดจ้าน ครบรส เปรี้ยว เผ็ด หอมสมุนไพร',
            price: 70,
            image: 'https://dummyimage.com/400x300'
          },
          {
            name: 'แกงเขียวหวานไก่',
            description: 'แกงเขียวหวานรสกลมกล่อม ใส่ไก่และมะเขือพวง',
            price: 65,
            image: 'https://dummyimage.com/400x300'
          },
          {
            name: 'กะเพราเนื้อไข่ดาว',
            description: 'ผัดกะเพราเนื้อรสจัดจ้าน เสิร์ฟพร้อมไข่ดาวกรอบๆ',
            price: 55,
            image: 'https://dummyimage.com/400x300'
          },
          {
            name: 'ส้มตำไทย',
            description: 'ส้มตำไทยเปรี้ยวหวาน เคียงถั่วลิสงและมะเขือเทศ',
            price: 40,
            image: 'https://dummyimage.com/400x300'
          }
    ]
  }),
  getters: {
    totalMenuItems: (state) => state.items.length
  },
  actions: {
    addItem(item) {
      this.items.push(item)
    }
  }
})
