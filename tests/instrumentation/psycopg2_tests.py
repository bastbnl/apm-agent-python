# -*- coding: utf-8 -*-


from unittest import TestCase
from opbeat.instrumentation.packages.psycopg2 import extract_signature


class ExtractSignatureTest(TestCase):
    def test_insert(self):
        sql = """INSERT INTO mytable (id, name) VALUE ('2323', 'Ron')"""
        actual = extract_signature(sql)

        self.assertEqual("INSERT INTO mytable", actual)

    def test_update(self):
        sql = """UPDATE mytable set name='Ron' WHERE id = 2323"""
        actual = extract_signature(sql)

        self.assertEqual("UPDATE mytable", actual)

    def test_delete(self):
        sql = """DELETE FROM mytable WHERE id = 2323"""
        actual = extract_signature(sql)

        self.assertEqual("DELETE FROM mytable", actual)

    def test_select_simple(self):
        sql = """SELECT id, name FROM mytable WHERE id = 2323"""
        actual = extract_signature(sql)

        self.assertEqual("SELECT FROM mytable", actual)

    def test_select_with_difficult_values(self):
        sql = """SELECT id, 'some name' + '" from Denmark' FROM "mytable" WHERE id = 2323"""
        actual = extract_signature(sql)

        self.assertEqual("SELECT FROM mytable", actual)

    def test_select_with_dollar_quotes(self):
        sql = """SELECT id, $$some single doubles ' $$ + '" from Denmark' FROM "mytable" WHERE id = 2323"""
        actual = extract_signature(sql)

        self.assertEqual("SELECT FROM mytable", actual)

    def test_select_with_difficult_table_name(self):
        sql = "SELECT id FROM \"myta\n-æøåble\" WHERE id = 2323"""
        actual = extract_signature(sql)

        self.assertEqual("SELECT FROM myta\n-æøåble", actual)

    def test_select_subselect(self):
        sql = """SELECT id, name FROM (
                SELECT id, 'not a FROM ''value' FROM mytable WHERE id = 2323
        ) LIMIT 20"""
        actual = extract_signature(sql)

        self.assertEqual("SELECT FROM mytable", actual)

    def test_select_with_invalid_subselect(self):
        sql = "SELECT id FROM (SELECT * FROM ..."""
        actual = extract_signature(sql)

        self.assertEqual("SELECT FROM", actual)

    def test_select_with_invalid_literal(self):
        sql = "SELECT 'neverending literal FROM (SELECT * FROM ..."""
        actual = extract_signature(sql)

        self.assertEqual("SELECT FROM", actual)

    def test_savepoint(self):
        sql = """SAVEPOINT x_asd1234"""
        actual = extract_signature(sql)

        self.assertEqual("SAVEPOINT", actual)

    def test_begin(self):
        sql = """BEGIN"""
        actual = extract_signature(sql)

        self.assertEqual("BEGIN", actual)
