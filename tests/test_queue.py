from unittest.case import TestCase

from mutantqueue.queue import PriorityQueue


class PriorityQueueTest(TestCase):
    def setUp(self):
        self.queue = PriorityQueue()

    def tearDown(self):
        self.queue.redis.delete(self.queue.key)

    def test_insert_add_element_to_sorted_set_with_correct_score(self):
        queue = PriorityQueue()
        queue.insert(10, 'member')

        self.assertEqual(queue.redis.zscore(queue.key, 'member'), 10)

    def test_pop_retrieve_and_remove_element_with_highest_score(self):
        queue = PriorityQueue()
        queue.insert(5, 'member1')
        queue.insert(15, 'member2')
        queue.insert(10, 'member3')

        self.assertEqual(queue.pop(), 'member2')

    def test_remove_remove_specified_element_from_queue(self):
        queue = PriorityQueue()
        queue.insert(5, 'member1', 10, 'member2', 10, 'member3')
        queue.remove('member1', 'member2')

        self.assertEqual(queue.size, 1)
        self.assertEqual(queue.redis.zscore(queue.key, 'member1'), None)
        self.assertEqual(queue.redis.zscore(queue.key, 'member2'), None)

    def test_size_returns_number_of_elements_in_sorted_set(self):
        queue = PriorityQueue()
        queue.insert(5, 'member1', 10, 'member2', 10, 'member3')

        self.assertEqual(queue.size, 3)
