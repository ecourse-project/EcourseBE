// =========================================== BASE ===========================================

export interface PaginationParams {
  limit: number;
  page: number;
}

export interface Pagination<T> {
  link: {
    next: string;
    previous: string;
  };
  count: number;
  results: Array<T>;
}

export enum SaleStatusEnum {
  AVAILABLE = 'AVAILABLE',
  IN_CART = 'IN_CART',
  PENDING = 'PENDING',
  BOUGHT = 'BOUGHT',
}

// ===========================================Users Auth===========================================
export interface IRegistration {
  email: string;
  password1: string;
  password2: string;
  full_name: string;
}

export interface ORegistration {
  email: string;
  full_name: string;
}

export interface IToken {
  email: string;
  password: string;
}

export interface OToken {
  refresh: string;
  access: string;
}

export interface ITokenRefresh {
  refresh: string;
}

export interface OTokenRefresh {
  access: string;
}

export interface OVerifyToken {
  detail?: string;
  code?: string;
}

// ===========================================Users===========================================

export enum RoleEnum {
  MANAGER='MANAGER',
  STUDENT='STUDENT',
}

export interface User {
  id: string;
  email: string;
  full_name: string;
  avatar: string;
  phone?: string;
  role: RoleEnum;
}

export interface OIsExist {
  exists: boolean;
}

export interface IPasswordRest {
  email: string;
}

export interface OPasswordRest {
  detail: string;
}

export interface IPasswordChange {
  old_password: string;
  password1: string;
  password2: string;
}

export interface OPasswordChange {
  detail: string;
}

// ===========================================Upload===========================================
export interface IFileUpload {
  file: string;
}

export interface OFileUpload {
  id: string;
  file_path: string;
  file_size: number;
  file_type: string;
  file_name: string;
  duration: number;
  file_embedded_url?: string;
  use_embedded_url?: boolean;
}

export interface IImageUpload {
  image: string;
  is_avatar?: boolean;
}

export interface OImageUpload {
  id: string;
  image_size: number;
  image_path: string;
  image_short_path: string;
  image_type: string;
  is_avatar: boolean;
}

export interface UploadImageSuccess {
  id: string;
  image_path: string;
  image_short_path: string;
  image_size: number;
  image_type: string;
  is_avatar: boolean;
}

// ===========================================Documents===========================================
export interface DocumentTopic {
  id: string;
  name: string;
}

export interface Document {
  id: string;
  created: string;
  modified: string;
  name: string;
  description: string;
  topic: string;
  price: number;
  sold: number;
  thumbnail: OImageUpload;
  file: OFileUpload;
  sale_status?: SaleStatusEnum;
  is_selling: boolean;
  views: number;
  // rating: number;
  num_of_rates: number;
  is_favorite?: boolean;
  // rating_detail?: Rating[];
  // my_rating?: Rating;
  download: boolean;
}

export interface IDocumentUpload {
  name: string;
  description: string;
  topic: string;
  price: number;
  image: string;
  file: string;
}

export interface ODocumentUpload {
  id: string;
  name: string;
  description: string;
  topic: string;
  price: number;
  sold: number;
  thumbnail: OImageUpload;
  file: OFileUpload;
  sale_status: string;
}

export interface Data {
  data: Document[];
}

export interface IDocumentUpdate {
  name: string;
  description: string;
  topic: string;
  price: number;
  image: string;
  file: string;
}

// ===========================================Courses===========================================
export enum ProgressStatusEnum {
  IN_PROGRESS = 'IN_PROGRESS',
  DONE = 'DONE',
}

export interface UpdateLessonArgs {
  lesson_id: string;
  completed_docs: string[];
  completed_videos: string[];
}

export interface UpdateProgressArgs {
  course_id: string;
  lessons: UpdateLessonArgs[];
}

export interface CourseDocument {
  id: string;
  modified: string;
  name: string;
  description: string;
  topic: string;
  file: OFileUpload;
}

export interface Topic {
  id: string;
  name: string;
}

export interface Lesson {
  id: string;
  name: string;
  lesson_number: number;
  content: string;
  videos: OFileUpload[];
  documents: CourseDocument[];
  docs_completed?: string[];
  videos_completed?: string[];
  quiz_detail?: QuizResult;
  list_quiz: Quiz[];
  is_done_quiz: boolean;
}

export interface Course {
  id: string;
  modified: string;
  name: string;
  topic?: Topic;
  description?: string;
  price?: number;
  sold?: number;
  lessons?: Lesson[];
  progress?: number;
  status?: ProgressStatusEnum;
  thumbnail?: OImageUpload;
  sale_status?: SaleStatusEnum;
  // views: number;
  // rating: number;
  // num_of_rates: number;
  mark?: number;
  is_done_quiz?: boolean;
  is_favorite?: boolean;
  // rating_detail?: Rating[];
  // my_rating?: Rating;
  // rating_stats?: RatingStats;
  request_status?: RequestStatus;
  course_of_class?: boolean;
  test: boolean;
}

// ===========================================Classes===========================================
export enum RequestStatus {
  ACCEPTED = 'accepted',
  REQUESTED = 'requested',
  AVAILABLE = 'available',
}

export interface Class {

}

// ===========================================Comments===========================================
export interface ReplyComment {
  id: string;
  user: User;
  created: string;
  content: string;
}

export interface CourseComment {
  id: string;
  user: User;
  created: string;
  content: string;
  course_id: string;
  reply_comments: ReplyComment[];
}

// ===========================================Cart===========================================
export enum MoveEnum {
  LIST = 'LIST',
  CART = 'CART',
  FAVORITE = 'FAVORITE',
}

export interface OCart {
  id: string;
  total_price: number;
  documents: Document[];
  courses: Course[];
}

export interface FavoriteList {
  id: string;
  documents: Document[];
  courses: Course[];
}

export interface OutputAdd {
  message: string;
}

export interface OutputRemove {
  message: string;
}

// ===========================================Payment===========================================
export interface CreateOrderArg {
  documents: string[];
  courses: string[];
  total_price: number;
}

export interface OutputOrder {
  id: string;
  created: string;
  code: string;
  total_price: number;
  documents: Document[];
  courses: Course[];
  status: string;
}

export interface OutputCancel {
  message: string;
}

export interface CalculatePriceArgs {
  documents: string[];
  courses: string[];
}

export interface TotalPrice {
  total_price: number;
}

// ===========================================Rating===========================================
export enum RatingEnum {
  ONE = 1,
  TWO = 2,
  THREE = 3,
  FOUR = 4,
  FIVE = 5,
}

export interface UserRatingInfo {
  full_name: string;
  avatar: string;
}

export interface RateDocArgs {
  document_id: string;
  // rating: RatingEnum;
  comment: string;
}

export interface RateCourseArgs {
  course_id: string;
  // rating: RatingEnum;
  comment: string;
}

export interface Rating {
  id: string;
  created: string;
  user: UserRatingInfo;
  // rating: RatingEnum;
  comment: string;
}

export interface RatingStats {
  score_1: number;
  score_2: number;
  score_3: number;
  score_4: number;
  score_5: number;
}

// ===========================================Quiz===========================================
export enum QuestionTypeEnum {
  CHOICES = 'CHOICES',
  MATCH = 'MATCH',
  FILL = 'FILL',
}

export enum ContentTypeEnum {
  TEXT = 'TEXT',
  IMAGE = 'IMAGE',
}

export interface MatchQuestion {
  order?: number;
  time_limit?: number;
  content: string;
  first_column: Array<{id: string, content_type: ContentTypeEnum, content: string}>;
  second_column: Array<{id: string, content_type: ContentTypeEnum, content: string}>;
  correct_answer?: Array<Array<string>>;
}

export interface FillBlankQuestion {
  order?: number,
  time_limit?: number,
  content: string;
  hidden_words?: Array<{id: number, word: string, hidden: boolean}>;
}

export interface ChoicesQuestion {
  order?: number;
  time_limit?: number;
  content: string;
  content_type?: ContentTypeEnum;
  choices: Array<{choice?: string, choice_name: string, answer_type: ContentTypeEnum, answer: string}>
}

export interface Quiz {
  id: string;
  order: number;
  time_limit?: number;
  question_type: QuestionTypeEnum;
  choices_question?: ChoicesQuestion;
  match_question?: MatchQuestion;
  fill_blank_question?: FillBlankQuestion;

}

export interface UserAnswersArgs {
  quiz_id: string;
  question_type: QuestionTypeEnum;
  answer: string | Array<string> | Array<Array<string>>;
}

export interface QuizResultArgs {
  course_id: string;
  lesson_id: string;
  user_answers: UserAnswersArgs[];
}

export interface CreateQuizArgs {
  course_id: string;
  lesson_id: string;
  choices_question: Array<ChoicesQuestion>;
  match_question: Array<MatchQuestion>;
  fill_blank_question: Array<FillBlankQuestion>;
}

export interface ChoicesQuizAnswer {
  correct: number;
  total: number;
  result: Array<{quiz_id: string, user_answer: string, correct_answer?: string}>;
}

export interface MatchQuizAnswer {
  quiz_id: string;
  correct: number;
  total: number;
  user_answer: Array<Array<string>>;
  correct_answer?: Array<Array<string>>;
}

export interface FillQuizAnswer {
  quiz_id: string;
  correct: number;
  total: number;
  user_answer: Array<string>;
  correct_answer?: Array<string>;
}

export interface QuizResult {
  mark?: number;
  choices_quiz: ChoicesQuizAnswer;
  match_quiz: MatchQuizAnswer[];
  fill_quiz: FillQuizAnswer[];
}

// ===========================================Setting===========================================
export enum NavTypeEnum {
  DOCUMENT = 'DOCUMENT',
  COURSE = 'COURSE',
  CLASS = 'CLASS',
  POST = 'POST',
}

export interface Topic {
  label: string;
  value: string;
}

export interface Nav {
  header: string;
  topic: Topic[];
  type: NavTypeEnum;
}

export interface HomepageDetail {
  document_id: string[];
  course_id: string[];
  class_id: string[];
  post_id: string[];

}

export interface Homepage {
  topic: string;
  detail: HomepageDetail;
}

// ===========================================Post===========================================
export interface Post {
  id: string;
  created?: string;
  modified?: string;
  name: string;
  topic?: string;
  thumbnail: OImageUpload;
  content?: string;
  content_summary: string;
}


// ===========================================Configuration===========================================
export interface PaymentInfo {
  method: string;
  payment_info: string;
  content: string;
}

const parseParamsToUrL = (url: string, params: string[], paramsName: string) => {
  let newURL = url;
  const newParams = [...params];
  newURL += `&${paramsName}=${newParams.shift()}`;
  for (const i of newParams) {
    newURL += `&${paramsName}=${i}`;
  }
  return newURL;
};



export const apiURL = {
  login: () => 'api/users-auth/token/',
  refresh: () => 'api/users-auth/token/refresh/',
  userInfo: (user_id) => `api/users/user-info/?user_id=${user_id}`,
  me: () => 'api/users/me/',
  register: () => 'api/users-auth/registration/',
  existEmail: (email) => `api/users/exists/?email=${email}`,
  resetPwd: () => 'api/users/password-reset/',
  changePwd: () => 'api/users/password-change/',
  verifyToken: () => `api/users-auth/token/verify/`,

  getHomeDocs: (limit, page, topic?, document_id?: string[]) => {
    let url = `api/documents/home/?limit=${limit}&page=${page}&topic=${topic}`;
    if (document_id) {
      url = parseParamsToUrL(url, document_id, `document_id`);
    }
    return url;
  },
  getAllDocs: (limit, page, topic?, document_id?: string[]) => {
    let url = `api/documents/?limit=${limit}&page=${page}&topic=${topic}`;
    if (document_id) {
      url = parseParamsToUrL(url, document_id, `document_id`);
    }
    return url;
  },
  getMostDownloadDocs: () => `api/documents/most-download/`,
  getUDocs: (limit, page) => `api/documents/my-documents/?limit=${limit}&page=${page}`,
  getDocDetail: (id) => `api/documents/detail/?document_id=${id}`,

  getCart: () => `api/carts/info/`,
  getFavoriteList: () => `api/carts/favorite/info/`,
  moveDoc: (id, start, end) => `api/carts/document/move/?document_id=${id}&start=${start}&end=${end}`,
  moveCourse: (id, start, end) => `api/carts/course/move/?course_id=${id}&start=${start}&end=${end}`,

  getAllOrders: (limit, page) => `api/payment/orders/?limit=${limit}&page=${page}`,
  getOrder: (id) => `api/payment/order/detail/?order_id=${id}`,
  createOrder: () => `/api/payment/order/create/`,
  cancelOrder: (id) => `api/payment/order/cancel/?order_id=${id}`,
  calculatePrice: () => `api/payment/order/calculate/`,

  getListCourses: () => `api/courses/all/`,
  getHomeCourses: (limit, page, topic?, course_id?: string[]) => {
    let url = `api/courses/home/?limit=${limit}&page=${page}&topic=${topic}`;
    if (course_id) {
      url = parseParamsToUrL(url, course_id, `course_id`);
    }
    return url;
  },
  getAllCourses: (limit, page, topic?, course_id?: string[]) => {
    let url = `api/courses/?limit=${limit}&page=${page}&topic=${topic}`;
    if (course_id) {
      url = parseParamsToUrL(url, course_id, `course_id`);
    }
    return url;
  },
  getMostDownloadCourses: () => `api/courses/most-download/`,
  getUCourses: (limit, page) => `api/courses/my-courses/?limit=${limit}&page=${page}`,
  getCourseDetail: (id) => `api/courses/detail/?course_id=${id}`,
  updateLessonProgress: () => `api/courses/update-lesson-progress/`,

  createComment: () => `api/comments/create/`,
  listComments: (id, limit, page) => `api/comments/list/?course_id=${id}&limit=${limit}&page=${page}`,

  rateDocument: () => `api/rating/document/rate/`,
  rateCourse: () => `api/rating/course/rate/`,
  documentRatingStats: (document_id) => `document/rating/stats/?document_id=${document_id}`,
  courseRatingStats: (course_id) => `course/rating/stats/?course_id=${course_id}`,
  documentRatingFilter: (document_id, score) => `document/rating/filter/?document_id=${document_id}&score=${score}`,
  courseRatingFilter: (course_id, score) => `course/rating/filter/?course_id=${course_id}&score=${score}`,

  createQuiz: () => `api/quiz/create/`,
  listQuiz: (course_id, lesson_id) => `api/quiz/?course_id=${course_id}&lesson_id=${lesson_id}`,
  getQuizResult: () => `api/quiz/result/`,
  downloadCerti: (course_id) => `api/quiz/certi/?course_id=${course_id}`,
  quizStartTime: (course_id, lesson_id, is_start) => `api/quiz/start-time/?course_id=${course_id}&lesson_id=${lesson_id}&is_start=${is_start}`,

  listHeaders: () => `api/settings/headers/`,
  getHome: () => `api/settings/home/`,
  initData: () => `api/settings/init/`,

  getHomeClasses: (limit, page, topic?, class_id?: string[]) => {
    let url = `api/classes/home/?limit=${limit}&page=${page}&topic=${topic}`;
    if (class_id) {
      url = parseParamsToUrL(url, class_id, `class_id`);
    }
    return url;
  },
  listClasses: (limit, page, topic?, class_id?: string[]) => {
    let url = `api/classes/?limit=${limit}&page=${page}&topic=${topic}`;
    if (class_id) {
      url = parseParamsToUrL(url, class_id, `class_id`);
    }
    return url;
  },
  getClassDetail: (class_id) => `api/classes/detail/?class_id=${class_id}`,
  requestJoinClass: () => `api/classes/join-request/`,
  updateClassProgress: () => `api/classes/update-lesson-progress/`,

  getPostDetail: (post_id) => `api/posts/detail/?post_id=${post_id}`,
  listPosts: (limit, page, topic?, header?, post_id?: string[]) => {
    let url = `api/posts/?limit=${limit}&page=${page}&topic=${topic}&header=${header}`;
    if (post_id) {
      url = parseParamsToUrL(url, post_id, `post_id`);
    }
    return url;
  },
  listPostTopics: () =>  `api/posts/topics/`,

  getPaymentInfo: () => `api/configuration/payment-info/`,

  uploadImage: () => 'api/upload/upload-images/',
};

class CourseService {
  static myInfo(): Promise<User> {
    return apiClient.get(apiURL.me());
  }

  static userInfo(user_id: string): Promise<User> {
    return apiClient.get(apiURL.userInfo(user_id));
  }

  static updateInfo(phone?: string, full_name?: string, avatar?: string): Promise<User> {
    return apiClient.patch(apiURL.me(), {
        phone: phone,
        full_name: full_name,
        avatar: avatar,
    });
  }

  static register(email: string, password1: string, password2: string, full_name: string): Promise<ORegistration> {
    return apiClient.post(apiURL.register(), {
      email: email,
      password1: password1,
      password2: password2,
      full_name: full_name,
    });
  }

  static existEmail(email: string): Promise<OIsExist> {
    return apiClient.get(apiURL.existEmail(email));
  }

  static resetPwd(email: string): Promise<OPasswordRest> {
    return apiClient.post(apiURL.resetPwd(), { email: email });
  }

  static changePwd(old_password: string, password1: string, password2: string): Promise<OPasswordChange> {
    return apiClient.patch(apiURL.changePwd(), {
      old_password: old_password,
      password1: password1,
      password2: password2,
    });
  }

  static verifyToken(token: string): Promise<OVerifyToken> {
    return apiClient.post(apiURL.verifyToken(), { token: token });
  }

  static getAllDocs(params: PaginationParams, topic?: string, document_id?: string[]): Promise<Pagination<Document>> {
    return apiClient.get(apiURL.getAllDocs(params.limit, params.page, topic, document_id));
  }

  static getHomeDocs(params: PaginationParams, topic?: string, document_id?: string[]): Promise<Pagination<Document>> {
    return apiClient.get(apiURL.getHomeDocs(params.limit, params.page, topic, document_id));
  }

  static getMostDownloadDocs(): Promise<Document[]> {
    return apiClient.get(apiURL.getMostDownloadDocs());
  }

  static getUserDocs(params: PaginationParams): Promise<Pagination<Document>> {
    return apiClient.get(apiURL.getUDocs(params.limit, params.page));
  }

  static getDocDetail(id: string): Promise<Document> {
    return apiClient.get(apiURL.getDocDetail(id));
  }

  // static updateDoc(id: string): Promise<Document> {
  // 	return apiClient.patch(apiURL.getDocDetail(id));
  // }

  static deleteDoc(id: string): Promise<any> {
    return apiClient.delete(apiURL.getDocDetail(id));
  }

  static getCart(): Promise<OCart> {
    return apiClient.get(apiURL.getCart());
  }

  static getFavoriteList(): Promise<FavoriteList> {
    return apiClient.get(apiURL.getFavoriteList());
  }

  static moveDoc(id: string, start: MoveEnum, end: MoveEnum): Promise<Document> {
    return apiClient.get(apiURL.moveDoc(id, start, end));
  }

  static moveCourse(id: string, start: MoveEnum, end: MoveEnum): Promise<Course> {
    return apiClient.get(apiURL.moveCourse(id, start, end));
  }

  static getAllOrders(params: PaginationParams): Promise<Pagination<OutputOrder>> {
    return apiClient.get(apiURL.getAllOrders(params.limit, params.page));
  }

  static getOrder(id: string): Promise<OutputOrder> {
    return apiClient.get(apiURL.getOrder(id));
  }

  static createOrder(params: CreateOrderArg): Promise<OutputOrder> {
    return apiClient.post(apiURL.createOrder(), params);
  }

  static cancelOrder(id: string): Promise<OutputCancel> {
    return apiClient.get(apiURL.cancelOrder(id));
  }

  static calculatePrice(params: CalculatePriceArgs): Promise<TotalPrice> {
    return apiClient.post(apiURL.calculatePrice(), params);
  }

  static getListCourses(): Promise<{id: string, course_of_class: boolean, name: string, lessons?: Array<{id: string, name: string}>}> {
    return apiClient.get(apiURL.getListCourses());
  }

  static getAllCourses(params: PaginationParams, topic?: string, course_id?: string[]): Promise<Pagination<Course>> {
    return apiClient.get(apiURL.getAllCourses(params.limit, params.page, topic, course_id));
  }

  static getHomeCourses(params: PaginationParams, topic?: string, course_id?: string[]): Promise<Pagination<Course>> {
    return apiClient.get(apiURL.getHomeCourses(params.limit, params.page, topic, course_id));
  }

  static getMostDownloadCourses(): Promise<Course[]> {
    return apiClient.get(apiURL.getMostDownloadCourses());
  }

  static getUserCourses(params: PaginationParams): Promise<Pagination<Course>> {
    return apiClient.get(apiURL.getUCourses(params.limit, params.page));
  }

  static getCourseDetail(id: string): Promise<Course> {
    return apiClient.get(apiURL.getCourseDetail(id));
  }

  static updateLessonProgress(params: UpdateProgressArgs): Promise<Course> {
    return apiClient.post(apiURL.updateLessonProgress(), params);
  }

  static createComment(owner_id: string, course_id: string, user_id: string, content: string): Promise<CourseComment> {
    return apiClient.post(apiURL.createComment(), {
      owner_id: owner_id,
      course_id: course_id,
      user_id: user_id,
      content: content,
    });
  }

  static listComments(id: string, limit: number, page: number): Promise<Pagination<CourseComment>> {
    return apiClient.get(apiURL.listComments(id, limit, page));
  }

  static rateDocument(params: RateDocArgs): Promise<Rating> {
    return apiClient.post(apiURL.rateDocument(), params);
  }

  static rateCourse(params: RateCourseArgs): Promise<Rating> {
    return apiClient.post(apiURL.rateCourse(), params);
  }

  static documentRatingStats(document_id: string): Promise<RatingStats> {
    return apiClient.get(apiURL.documentRatingStats(document_id));
  }

  static courseRatingStats(course_id: string): Promise<RatingStats> {
    return apiClient.get(apiURL.courseRatingStats(course_id));
  }

  static documentRatingFilter(document_id: string, score: RatingEnum): Promise<Rating> {
    return apiClient.get(apiURL.documentRatingFilter(document_id, score));
  }

  static courseRatingFilter(course_id: string, score: RatingEnum): Promise<Rating> {
    return apiClient.get(apiURL.courseRatingFilter(course_id, score));
  }

  static createQuiz(params: CreateQuizArgs): Promise<{}> {
    return apiClient.post(apiURL.createQuiz(), params);
  }

  static listQuiz(course_id: string, lesson_id: string): Promise<Quiz[]> {
    return apiClient.get(apiURL.listQuiz(course_id, lesson_id));
  }

  static getQuizResult(params: QuizResultArgs): Promise<QuizResult> {
    return apiClient.post(apiURL.getQuizResult(), params);
  }

  static downloadCerti(course_id: string): Promise<any> {
    return apiClient.get(apiURL.downloadCerti(course_id));
  }

  static quizStartTime(course_id: string, lesson_id: string, is_start: boolean): Promise<{start_time?: string}> {
    return apiClient.get(apiURL.quizStartTime(course_id, lesson_id, is_start));
  }

  static listHeaders(): Promise<Nav[]> {
    return apiClient.get(apiURL.listHeaders());
  }

  static getHome(): Promise<Homepage[]> {
    return apiClient.get(apiURL.getHome());
  }

  static initData(): Promise<{"success": true}> {
    return apiClient.get(apiURL.initData());
  }

  static getHomeClasses(limit: number, page: number, topic?: string, class_id?: string[]): Promise<Pagination<Course>> {
    return apiClient.get(apiURL.getHomeClasses(limit, page, topic, class_id));
  }

  static listClasses(limit: number, page: number, topic?: string, class_id?: string[]): Promise<Pagination<Course>> {
    return apiClient.get(apiURL.listClasses(limit, page, topic, class_id));
  }

  static getClassDetail(class_id: string): Promise<Course> {
    return apiClient.get(apiURL.getClassDetail(class_id));
  }

  static requestJoinClass(class_id: string): Promise<{ request_status: RequestStatus }> {
    return apiClient.post(apiURL.requestJoinClass(), { class_id: class_id });
  }

  static listPosts(limit: number, page: number, topic?: string, header?: string, post_id?: string[]): Promise<Pagination<Post>> {
    return apiClient.get(apiURL.listPosts(limit, page, topic, header, post_id));
  }

  static getPostDetail(post_id: string): Promise<Post> {
    return apiClient.get(apiURL.getPostDetail(post_id));
  }

  static listPostTopics(): Promise<string[]> {
    return apiClient.get(apiURL.listPostTopics());
  }

  static updateClassProgress(params: UpdateProgressArgs): Promise<Course> {
    return apiClient.post(apiURL.updateClassProgress(), params);
  }

  static getPaymentInfo(): Promise<PaymentInfo> {
    return apiClient.get(apiURL.getPaymentInfo());
  }

  static uploadImage(data: any): Promise<any> {
    return apiClient.post(apiURL.uploadImage(), data);
  }
}
export default CourseService;