// =========================================== BASE ===========================================

export interface PaginationParams {
    limit: number;
    page: number;
}

export interface Pagination<T> {
  link: {
      "next": string;
      "previous": string;
  }
  count: number;
  results: Array<T>;
}

export enum SaleStatusEnum {
  AVAILABLE = 'AVAILABLE',
  IN_CART = 'IN_CART',
  PENDING = 'PENDING',
  BOUGHT = 'BOUGHT'
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


// ===========================================Users===========================================
export interface User {
    id: string;
    email: string;
    full_name: string;
    avatar: string;
    phone: string;
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
    file_size: string;
    file_type: string;
    file_name: string;
    duration: number;
}

export interface IImageUpload {
    file: string;
}

export interface OImageUpload {
    id: string;
    image_path: string;
    image_size: string;
    image_type: string;
}


// ===========================================Documents===========================================
export interface Document {
    id: string;
    created: string;
    modified: string;
    name: string;
    description: string;
    title: string;
    price: number;
    sold: number;
    thumbnail: OImageUpload;
    file: OFileUpload;
    sale_status: SaleStatusEnum;
    is_selling: boolean;
    views: number;
    rating: number;
    num_of_rates: number;
    is_favorite: boolean;
}

export interface IDocumentUpload {
    name: string;
    description: string;
    title: string;
    price: number;
    image: string;
    file: string;
}

export interface ODocumentUpload {
    id: string;
    name: string;
    description: string;
    title: string;
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
    title: string;
    price: number;
    image: string;
    file: string;
}

// ===========================================Courses===========================================
export enum ProgressStatusEnum {
    IN_PROGRESS = 'IN_PROGRESS',
    DONE = 'DONE'
}

export interface UpdateProgressOutput {
    is_completed: boolean;
}


export interface CourseDocument {
    id: string;
    created: string;
    modified: string;
    name: string;
    description: string;
    title: string;
    file: OFileUpload;
}

export interface Topic {
    id: string;
    created: string;
    modified: string;
    name: string;
}

export interface Lesson {
    id: string;
    created: string;
    modified: string;
    name: string;
    lesson_number: number;
    content: string;
    videos: OFileUpload[];
    documents: CourseDocument[];
    progress: number;
}

export interface Course {
    id: string;
    created: string;
    modified: string;
    name: string;
    topic: Topic;
    description: string;
    price: number;
    sold: number;
    lessons: Lesson[],
    progress: number;
    status: ProgressStatusEnum;
    thumbnail: OImageUpload;
    sale_status: SaleStatusEnum;
    is_selling: boolean;
    views: number;
    rating: number;
    num_of_rates: number;
    mark: number;
    is_done_quiz: boolean;
    is_favorite: boolean;
    docs_completed: string[],
    videos_completed: string[],
}


// ===========================================Comments===========================================
export interface ReplyComment {
    id: string;
    user: User;
    content: string;
}

export interface Comment {
    id: string;
    user: User;
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
    message: string
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
  FIVE = 5
}

export interface RateDocArgs {
    document_id: string;
    rating: RatingEnum;
}

export interface RateCourseArgs {
    course_id: string;
    rating: RatingEnum;
}

export interface Rating {
    id: string;
    created: string;
    modified: string;
    user: User;
    rating: RatingEnum;
}




const apiURL = {
	login: () => 'api/users-auth/token/',
	me: () => 'api/users/me/',
	register: () => 'api/users-auth/registration/',
	existEmail: (email) => `api/users/exists/?email=${email}`,
	resetPwd: () => 'api/users/password-reset/',
	changePwd: () => 'api/users/password-change/',

    getAllDocs: (limit, page) => `api/documents/?limit=${limit}&page=${page}`,
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

    getAllCourses: (limit, page) => `api/courses/?limit=${limit}&page=${page}`,
    getMostDownloadCourses: () => `api/courses/most-download/`,
    getUCourses: (limit, page) => `api/courses/my-courses/?limit=${limit}&page=${page}`,
    getCourseDetail: (id) => `api/courses/detail/?course_id=${id}`,
    UpdateCourseDocumentProgress: (course_id, doc_id) => `api/courses/course-progress/document/?course_id=${course_id}&course_doc_id=${doc_id}`,
    UpdateCourseVideoProgress: (course_id, file_id) => `api/courses/course-progress/video/?course_id=${course_id}&file_id=${file_id}`,

    createComment: () => `api/comments/create/`,
    listComments: (id) => `api/comments/list/?course_id=${id}`,

    rateDocument: () => `api/rating/document/rate/`,
    rateCourse: () => `api/rating/course/rate/`,
};


class CourseService {
    static myInfo(): Promise<User> {
		return apiClient.get(apiURL.me());
	}

    static register(email: string, password1: string, password2: string, full_name: string): Promise<ORegistration> {
        return apiClient.post(apiURL.register(), {email: email, password1: password1, password2: password2, full_name: full_name})
    }

    static existEmail(email: string): Promise<OIsExist> {
		return apiClient.get(apiURL.existEmail(email));
	}

    static resetPwd(email: string) : Promise<OPasswordRest> {
		return apiClient.post(apiURL.resetPwd(), {email: email});
	}

    static changePwd(old_password: string, password1: string, password2: string) : Promise<OPasswordChange> {
		return apiClient.post(apiURL.changePwd(), {old_password: old_password, password1: password1, password2: password2});
	}

	static getAllDocs(params: PaginationParams): Promise<Pagination<Document>> {
		return apiClient.get(apiURL.getAllDocs(params.limit, params.page));
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

    static getAllCourses(params: PaginationParams): Promise<Pagination<Course>> {
		return apiClient.get(apiURL.getAllCourses(params.limit, params.page));
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

    static UpdateCourseDocumentProgress(course_id: string, doc_id: string): Promise<UpdateProgressOutput> {
        return apiClient.get(apiURL.UpdateCourseDocumentProgress(course_id, doc_id));
    }

    static UpdateCourseVideoProgress(course_id: string, file_id: string): Promise<UpdateProgressOutput> {
        return apiClient.get(apiURL.UpdateCourseVideoProgress(course_id, file_id));
    }

    static createComment(owner_id: string, course_id: string, user_id: string, content: string) : Promise<Comment> {
		return apiClient.post(apiURL.createComment(), {owner_id: owner_id, course_id: course_id, user_id: user_id, content: content});
	}

    static listComments(id: string): Promise<Comment[]> {
		return apiClient.get(apiURL.listComments(id));
	}

    static rateDocument(params: RateDocArgs): Promise<Rating> {
        return apiClient.post(apiURL.rateDocument(), params);
    }

    static rateCourse(params: RateCourseArgs): Promise<Rating> {
        return apiClient.post(apiURL.rateCourse(), params);
    }
}
export default CourseService;