export const TOPICS = [
  'คดีความ-นักศึกษา',
  'การบริหารการจัดการ',
  'การเมือง',
  'วิชาการ/การวิจัย',
  'คดีความ-บุคลากร',
  'ทุจริต/ฉ้อโกง',
  'อื่นๆ'
]

export const UNSPECIFIED_TOPIC = 'ไม่ระบุ'

export const topicOf = (issue) => issue.topic || UNSPECIFIED_TOPIC
